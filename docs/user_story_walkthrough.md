# User Story Walkthrough (Endpoint by Endpoint)

## 1. Customer Discovers the Buylist
- `GET /buylist/products` — Customer browses available cards using filters.
- `GET /buylist/settings` — Frontend retrieves store policies and drop-off options.
- `GET /buylist/products/{internalId}` — Customer reviews details for each card before adding to cart.

## 2. Customer Builds and Submits a Cart
- `GET /carts/current` — Load any in-progress draft cart.
- `POST /carts` — Save cart changes while selecting conditions and quantities.
- `POST /auth/register` or `POST /auth/login` — Authenticate as needed (optional for guests depending on configuration).
- `POST /carts/submit` — Validate limits, lock pricing, and transition cart to `submitted` status.
- Notification is sent via internal messaging queue/integration (future enhancement).

## 3. Employee Intake & Processing
- `GET /carts?status=submitted` — Employee dashboard shows carts awaiting action.
- `POST /processing/{cartId}/accept` — Employee claims the cart for processing.
- `POST /processing/{cartId}/items` — Record actual verified card conditions and quantities.
- `POST /processing/{cartId}/attachments` — Upload photos or supporting documents (if necessary).
- `POST /processing/{cartId}/complete` — Finalize payouts, update history, and set status to `processed`.

## 4. Manager Review & Corrections
- `GET /inventory/processed` — Manager views processed carts pending review.
- `GET /carts/{cartId}` — Manager reviews detailed processing history.
- `POST /inventory/review/{cartId}` — Apply corrections for discrepancies or policy adjustments.

## 5. Inventory Import Preparation
- `POST /inventory/finalize` — Select reviewed carts to create an `inventory_imports` batch.
- `GET /inventory/imports/{importId}` — Review aggregated totals and ensure data accuracy.

## 6. Export & Completion
- `GET /inventory/export/{importId}` — Generate formatted export (e.g., Shopify CSV) for downstream systems.
- `PATCH /inventory/imports/{importId}` (future) — Mark export as synced once imported into external inventory.
- `GET /inventory/imports` — Track import history and completion status.

## 7. Continuous Improvement & Administration
- `GET /admin/buylist` — Administrators adjust pricing and availability.
- `POST /admin/buylist` — Update price overrides and multipliers based on analytics.
- `GET /admin/settings` / `PATCH /admin/settings` — Modify store-wide policies and configuration.
- `POST /admin/emergency-disable` — React quickly to market shifts by disabling categories or groups.
- `GET /analytics/spend-summary` — Monitor spend trends to guide future buylist decisions.
- `GET /admin/audit-logs` — Review actions for compliance and troubleshooting.
