# Backend Endpoints

## Authentication & Users
- `POST /auth/register` — Create new customer accounts; validates configuration for allowing registrations.
- `POST /auth/login` — Authenticate users and issue JWT tokens.
- `POST /auth/refresh` — Refresh JWT access tokens using refresh tokens.
- `GET /users/me` — Retrieve the authenticated user's profile and role.
- `GET /users` (admin) — List users with pagination and filters.
- `PATCH /users/{userId}` (admin) — Update role, status, or reset passwords.

## Public Buylist
- `GET /buylist/products` — Searchable list of active buylist entries with filters (category, group, price range, text query).
- `GET /buylist/products/{internalId}` — Detailed product data including pricing, limits, and availability.
- `GET /buylist/settings` — Exposes public configuration (store info, drop-off options, credit bonus).

## Cart Management
- `GET /carts/current` — Fetch the authenticated customer's draft cart.
- `POST /carts` — Create or update a draft cart with items, drop-off preference, and notes.
- `POST /carts/submit` — Validate and submit the current cart for processing.
- `GET /carts/{cartId}` — Retrieve a specific cart with full history and status.
- `GET /carts` (employee/manager) — List carts filtered by status (submitted, accepted, processed, etc.).
- `POST /carts/{cartId}/cancel` — Cancel a cart by customer or staff with reason logging.

## Employee Processing
- `POST /processing/{cartId}/accept` — Mark a submitted cart as accepted for processing.
- `POST /processing/{cartId}/items` — Record verified items, conditions, and payout adjustments.
- `POST /processing/{cartId}/complete` — Finalize processing, including payout summary and audit trail.
- `POST /processing/{cartId}/attachments` — Upload supporting documents or photos.

## Inventory Review & Intake
- `GET /inventory/processed` — List processed carts awaiting manager review.
- `POST /inventory/review/{cartId}` — Submit corrections to processed cart items and notes.
- `POST /inventory/finalize` — Confirm reviewed carts and create an inventory import batch.
- `GET /inventory/imports` — List historical import batches with status metadata.
- `GET /inventory/imports/{importId}` — View details of a specific import batch.
- `GET /inventory/export/{importId}` — Generate export files (CSV, JSON) for downstream systems.

## Buylist Configuration
- `GET /admin/buylist` — Administrative view of all buylist entries, including disabled items.
- `POST /admin/buylist` — Create or update buylist entries with price overrides and limits.
- `PATCH /admin/buylist/{internalId}/status` — Enable or disable a product.
- `GET /admin/progress` — Monitor buylist progress (max quantities, bought counts).
- `POST /admin/emergency-disable` — Disable an entire group or category immediately.
- `DELETE /admin/emergency-disable/{id}` — Remove an emergency disable rule.

## System Settings & Integrations
- `GET /admin/settings` — Retrieve server settings (store info, credit bonus, condition percentages).
- `PATCH /admin/settings` — Update server settings with validation and audit logging.
- `POST /admin/imports/tcgcsv` — Manually trigger a TCGCSV data import.
- `GET /admin/imports/tcgcsv/runs` — View history and status of scheduled imports.
- `GET /admin/audit-logs` — Query audit logs with filters (user, action, date range).

## Analytics
- `GET /analytics/spend-summary` — Aggregate spend and quantities by filters (category, group, product, date range).
- `GET /analytics/employee-performance` — Metrics on processing throughput and accuracy.
- `GET /analytics/inventory-impact` — Track inventory additions per import and product.

## Health & Utility
- `GET /health` — Service health check.
- `GET /metrics` — Prometheus-compatible metrics endpoint.
- `GET /docs` — API documentation explorer (Swagger/OpenAPI).
