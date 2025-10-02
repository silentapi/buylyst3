# TODO & Status Tracker

## Planning Documents
- [x] Create detailed planning documentation set (user story, features, endpoints, frontend pages, models, walkthrough, long-term plan).
- [x] Update README to reference new documents and summarize scope.
- [x] Establish repository-wide agent guidelines.

## Phase 0: Foundations
- [x] Define development environment setup instructions.
  - Documented in [docs/development_environment.md](docs/development_environment.md) covering prerequisites, environment variables, and launch commands.
  - Backend scaffold includes healthcheck endpoint for verifying environment wiring.
- [ ] Configure CI/CD pipeline (linting, testing, security scans).
- [ ] Provision shared MongoDB instances and seed datasets.
- [ ] Implement authentication scaffold (JWT, roles) in codebase.

## Phase 1: Public Buylist & Cart
- [ ] Integrate TCGCSV import scheduler.
- [ ] Build public buylist endpoints with filtering and search.
- [ ] Implement React pages for buylist browsing and product detail.
- [ ] Develop cart drafting and submission flow with validation.
- [ ] Add submission notifications and status tracker UI.

## Phase 2: Employee Processing
- [ ] Create employee queue and cart acceptance APIs/UI.
- [ ] Implement processing workspace with condition/payout tools.
- [ ] Enable attachment upload handling and storage.
- [ ] Expand audit logging for employee actions.

## Phase 3: Manager Review & Inventory Intake
- [ ] Build manager review dashboard and correction flows.
- [ ] Implement inventory import batch creation and tracking endpoints.
- [ ] Generate export files (Shopify CSV baseline) with validation.
- [ ] Add reconciliation tools comparing processed vs corrected data.

## Phase 4: Administration & Analytics
- [ ] Deliver buylist management UI with emergency disable controls.
- [ ] Implement system settings pages with guardrails and audit trails.
- [ ] Build analytics dashboards and supporting APIs.
- [ ] Introduce analytics caching and performance tuning.

## Phase 5: Deployment & Operations
- [ ] Prepare production deployment scripts (Docker/systemd) and documentation.
- [ ] Configure monitoring and alerting (metrics, logs, uptime checks).
- [ ] Establish backup/restore procedures for MongoDB and file storage.
- [ ] Conduct load testing and performance tuning sessions.
- [ ] Plan pilot rollout and feedback loop.

## Notes & Dependencies
- Align feature implementation with the [Long-Term Implementation Plan](docs/implementation_plan.md).
- Update relevant documents and this tracker immediately after each feature milestone progresses.
- Capture emerging risks, decisions, and follow-ups directly under the affected phase.
- Backend architecture reference added at [docs/backend_architecture.md](docs/backend_architecture.md); consult before modifying Flask modules or introducing new blueprints.
