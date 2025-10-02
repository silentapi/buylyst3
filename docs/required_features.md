# Required Features

## Public & Customer Experience
- Discoverable buylist with search, filters (category, group, rarity), and price indicators.
- Customer authentication with optional guest submission (respecting configuration).
- Cart builder with condition selection, quantity controls, and price validation.
- Submission workflow supporting shipping and in-store drop-off, including instructions and acknowledgments.
- Real-time status tracking and notifications for cart updates.

## Employee Operations
- Queue of submitted carts with prioritization and filtering.
- Cart processing workspace capturing condition verification, quantity adjustments, and payout calculations.
- Support for notes, discrepancies, and photo attachments.
- Ability to cancel carts or items with audit logging.

## Management & Inventory
- Review dashboard for processed carts awaiting correction or intake.
- Correction interface to adjust quantities, conditions, payouts, and add manager notes.
- Bulk finalize carts into inventory import batches with summary metrics.
- Export generation (e.g., Shopify CSV) with configurable templates.
- Post-export tracking of completed carts and import history.

## Administration & Configuration
- Buylist configuration tools (price overrides, multipliers, disabled items/groups/categories).
- System settings management (store info, credit bonus, condition percentages, drop-off options).
- Emergency disable controls and logging.
- User management (roles: customer, employee, manager, admin) with role-based access control.
- Audit log viewer with filtering and export.

## Data Integrations & Maintenance
- Scheduled imports from TCGCSV API with error handling and delta updates.
- Inventory export integrations with third-party systems.
- Analytics reporting for spend, category trends, employee performance, and inventory impact.
- Backup and restore procedures for MongoDB and configuration data.

## Non-Functional Requirements
- Secure authentication (JWT), HTTPS support, and least-privilege access.
- Responsive and accessible frontend (React + Tailwind).
- Observability: structured logging, metrics, and alerting.
- Scalability to handle multiple concurrent cart submissions and processing sessions.
- Comprehensive test coverage and CI/CD pipeline readiness.
