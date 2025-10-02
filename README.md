<div align="center">

# BuyLyst.co

</div>

BuyLyst.co is a full-stack Python + MongoDB + React application for trading card game stores to manage buylist intake, pricing, cart processing, and inventory importing. The platform enables customers to submit cards for sale, employees to validate physical cards, and managers to intake results into downstream inventory systems (e.g., Shopify).

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Planning Documents](#planning-documents)
- [Data Model Summary](#data-model-summary)
- [Endpoint Coverage Snapshot](#endpoint-coverage-snapshot)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

## Project Overview
- Self-hosted Flask server secured with JWT authentication and backed by MongoDB storage.
- Daily CSV imports from the TCGCSV API to keep product data up to date.
- Public buylist interface showing cards the store wants to buy with pricing enforcement.
- Advanced cart system supporting condition-based payouts and drop-off workflows.
- Administrative controls for pricing, progress tracking, and emergency disables.
- Employee and manager workflows covering intake, review, inventory exports, and auditing.

## Architecture
| Layer       | Stack / Tooling              |
|-------------|------------------------------|
| Backend     | Flask, Flask-JWT-Extended    |
| Database    | MongoDB                      |
| Scheduler   | APScheduler                  |
| Frontend    | React, Tailwind CSS (planned) |
| Deployment  | Bare metal / self-hosted     |

## Planning Documents
- [User Story Narrative](docs/user_story_narrative.md)
- [Required Features](docs/required_features.md)
- [Backend Endpoints](docs/backend_endpoints.md)
- [Frontend Pages](docs/frontend_pages.md)
- [Database Collections & Models](docs/database_models.md)
- [User Story Walkthrough](docs/user_story_walkthrough.md)
- [Long-Term Implementation Plan](docs/implementation_plan.md)

## Data Model Summary
- **products**: Imported from TCGCSV; includes IDs, taxonomy, metadata, and price metrics.
- **buylist_entries**: Store-defined pricing configuration and visibility controls per product.
- **buylist_progress**: Tracks pending and processed quantities relative to max thresholds.
- **buy_carts**: Customer submissions with status history, payouts, and processing details.
- **users**: Authentication records with roles and contact preferences.
- **server_settings**: Store policies, payout multipliers, and drop-off options.
- **audit_logs**: Immutable record of significant actions and changes.
- **emergency_disables**: Manual overrides for groups, categories, or specific products.
- **inventory_imports**: Aggregated processed carts prepared for downstream inventory syncs.
- **import_runs**: Execution metadata for scheduled data imports.
- **analytics_cache**: Materialized analytics results for performance.

## Endpoint Coverage Snapshot
| Feature | Status | Notes |
|---------|--------|-------|
| Search public buylist | ✅ Implemented | |
| Register/Login/Auth | ✅ Implemented | |
| Add to cart / view current cart / submit | ✅ Implemented | |
| Emergency disables (category/group) | ✅ Implemented | Product-level disable not yet supported |
| View pending carts (employee) | ✅ Implemented | |
| View single cart with discontinued detection | ✅ Implemented | |
| Process cart with conditions + payout | ✅ Implemented | |
| Cancel cart (customer or employee) | ✅ Implemented | |
| Inventory review workflow | 🟥 Missing | Needs step-by-step review logic |
| Inventory correction and cart intake | 🟥 Missing | Requires actual vs processed state |
| Inventory import + CSV export | 🟥 Missing | Format varies per POS |
| Audit logs for all actions | ✅ Implemented | |
| Admin UI for settings, emergency disable, progress, and buylist config | ✅ Implemented | |
| Analytics endpoints for spend tracking | 🟥 Missing | Need group/category/product filters |

## Roadmap
High-level phases and milestones are detailed in the [Long-Term Implementation Plan](docs/implementation_plan.md). Key near-term goals include completing the inventory review workflow, implementing export capabilities, and delivering analytics dashboards.

## Contributing
1. Fork the repository and create a feature branch.
2. Ensure planning documents remain updated for any scope changes.
3. Write tests and documentation for new functionality.
4. Submit a pull request describing changes, testing steps, and any migration considerations.
