"""Utility for scraping deck data from PiltoverArchive with verbose logging."""
from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass
from html import unescape
from typing import Iterator, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

logger = logging.getLogger("piltover.scraper")

DECK_LINK_RE = re.compile(
    r"<a[^>]+href=\"(?P<href>/decks/view/[0-9a-fA-F-\-]+)\"[^>]*>(?P<label>.*?)</a>",
    re.IGNORECASE | re.DOTALL,
)
LEGEND_IMG_RE = re.compile(r"<img[^>]+alt=\"(?P<alt>[^\"]+)\"", re.IGNORECASE)
NEXT_DATA_RE = re.compile(
    r"<script[^>]+id=\"__NEXT_DATA__\"[^>]*>(?P<payload>.*?)</script>",
    re.IGNORECASE | re.DOTALL,
)


@dataclass
class DeckCandidate:
    """Represents a potential deck discovered during scraping."""

    href: str
    label: Optional[str]
    source: str


class PiltoverArchiveScraper:
    """Scrape deck listings from PiltoverArchive with detailed logging."""

    def __init__(self, base_url: str = "https://piltoverarchive.com", timeout: float = 30.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        logger.debug(
            "Initialized PiltoverArchiveScraper for %s (timeout=%.1fs)",
            self.base_url,
            timeout,
        )

    def fetch_decks(self, format_slug: str = "standard", region: str = "americas") -> list[DeckCandidate]:
        """Fetch deck metadata from the leaderboard page."""
        path = "/decks"
        params = {"format": format_slug, "region": region}
        url = f"{self.base_url}{path}?{urlencode(params)}"
        logger.info("Fetching Piltover deck leaderboard from %s", url)

        html = self._http_get(url)
        if not html:
            logger.error("No HTML returned from deck leaderboard %s", url)
            return []

        deck_links = list(self._extract_decks_from_html(html))
        logger.info("Found %s deck link(s) directly in HTML", len(deck_links))

        if not deck_links:
            logger.warning(
                "Deck links were not present in the static HTML from %s. Checking embedded Next.js data for decks.",
                url,
            )
            deck_links = self._extract_decks_from_next_data(html)
            logger.info("Found %s deck candidate(s) within __NEXT_DATA__ JSON", len(deck_links))

        if not deck_links:
            logger.error("No decks discovered after HTML and JSON parsing attempts.")

        return deck_links

    def _http_get(self, url: str) -> str:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; BuyLystDeckScraper/1.0)"})
        start = time.perf_counter()
        try:
            with urlopen(request, timeout=self.timeout) as response:
                elapsed = time.perf_counter() - start
                status = getattr(response, "status", "?")
                headers = dict(response.headers.items())
                logger.info(
                    "Received HTTP %s from %s in %.2fs",
                    status,
                    url,
                    round(elapsed, 2),
                )
                logger.debug("Response headers from %s: %s", url, headers)
                body_bytes = response.read()
        except HTTPError as exc:
            logger.exception(
                "HTTP error while fetching Piltover deck leaderboard %s: %s (%s)",
                url,
                exc.code,
                exc.reason,
            )
            return ""
        except URLError as exc:
            logger.exception(
                "Network error while reaching Piltover deck leaderboard %s: %s",
                url,
                exc,
            )
            return ""

        body_preview = body_bytes[:500].decode("utf-8", errors="replace")
        logger.debug("HTML preview from %s:\n%s", url, body_preview)

        return body_bytes.decode("utf-8", errors="replace")

    def _extract_decks_from_html(self, html: str) -> Iterator[DeckCandidate]:
        logger.debug("Scanning HTML (%s characters) for direct deck links using regex pattern.", len(html))
        matches = list(DECK_LINK_RE.finditer(html))
        logger.debug("Regex matched %s potential deck anchors.", len(matches))

        for match in matches:
            href = match.group("href")
            label_fragment = match.group("label")
            label = self._clean_html_fragment(label_fragment)
            logger.debug(
                "Discovered deck anchor in HTML at %s with raw label fragment %r -> cleaned label %r",
                href,
                label_fragment[:120],
                label,
            )
            yield DeckCandidate(href=href, label=label, source="html-anchor")

        legends = LEGEND_IMG_RE.findall(html)
        if legends:
            logger.info(
                "Captured %s legend name(s) from <img alt> tags. Sample: %s",
                len(legends),
                legends[:5],
            )
            for legend in legends[:5]:
                logger.debug("Legend candidate discovered: %s", legend)
        else:
            logger.debug("No legend <img> tags detected in HTML.")

    def _extract_decks_from_next_data(self, html: str) -> list[DeckCandidate]:
        logger.debug("Looking for __NEXT_DATA__ JSON payload inside HTML.")
        match = NEXT_DATA_RE.search(html)
        if not match:
            script_count = html.lower().count("<script")
            logger.warning(
                "__NEXT_DATA__ script tag not found in HTML. Document contains %s <script> tag(s).",
                script_count,
            )
            return []

        payload = match.group("payload")
        logger.debug("Located __NEXT_DATA__ JSON payload with %s characters.", len(payload))

        try:
            data = json.loads(unescape(payload))
        except json.JSONDecodeError as exc:
            logger.exception(
                "Failed to decode __NEXT_DATA__ JSON payload (%s characters): %s",
                len(payload),
                exc,
            )
            return []

        logger.debug("Top-level __NEXT_DATA__ keys: %s", list(data.keys())[:10])

        results = list(self._walk_deck_candidates(data))
        logger.debug("Extracted %s deck candidate(s) while traversing JSON payload.", len(results))
        return results

    def _walk_deck_candidates(self, node: object, path: str = "root") -> Iterator[DeckCandidate]:
        if isinstance(node, dict):
            for key, value in node.items():
                next_path = f"{path}.{key}"
                if key.lower() in {"decks", "decklist", "decklists", "items", "results"} and isinstance(value, list):
                    logger.debug(
                        "Encountered list candidate for deck data at %s with %s entries.",
                        next_path,
                        len(value),
                    )
                yield from self._walk_deck_candidates(value, next_path)
        elif isinstance(node, list):
            for index, item in enumerate(node):
                next_path = f"{path}[{index}]"
                if isinstance(item, dict):
                    href = self._extract_href(item)
                    label = self._extract_label(item)
                    if href:
                        logger.info(
                            "Found deck candidate in JSON at %s: href=%s label=%s",
                            next_path,
                            href,
                            label,
                        )
                        yield DeckCandidate(href=href, label=label, source=next_path)
                yield from self._walk_deck_candidates(item, next_path)

    def _extract_href(self, candidate: dict) -> Optional[str]:
        for key in ("href", "url", "link", "path"):
            value = candidate.get(key)
            if isinstance(value, str) and "/decks/view/" in value:
                return value
        return None

    def _extract_label(self, candidate: dict) -> Optional[str]:
        for key in ("label", "name", "title", "legend", "deckName", "cardName"):
            value = candidate.get(key)
            if isinstance(value, str):
                return value
        return None

    def _clean_html_fragment(self, fragment: str | None) -> Optional[str]:
        if not fragment:
            return None
        text = re.sub(r"<[^>]+>", " ", fragment)
        text = re.sub(r"\s+", " ", text)
        return text.strip() or None


def run_cli() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    scraper = PiltoverArchiveScraper()
    decks = scraper.fetch_decks()
    logger.info("Scraping finished with %s deck candidate(s).", len(decks))
    for deck in decks:
        logger.info(
            "Deck candidate -> href=%s label=%s source=%s",
            deck.href,
            deck.label,
            deck.source,
        )


if __name__ == "__main__":
    run_cli()
