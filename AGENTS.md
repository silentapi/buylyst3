# Agent Guidelines

## Repository-Wide Expectations
- Maintain the planning documents in the `docs/` directory. Update them whenever scope, features, or architecture change.
- Keep `README.md` aligned with the current state of the project and reference newly added documents.
- Preserve the data model and endpoint summaries when expanding functionality.
- Document every new model, endpoint, or noteworthy architectural detail in the appropriate `docs/` reference and link to it here. Future contributors must review those documents before modifying the scoped areas.

## TODO Management
- Always keep `TODO.md` up to date with feature status, milestones, and notes for future developers.
- Update TODO items immediately after any relevant code or documentation changes.
- Include context such as blockers, dependencies, and links to corresponding documents or tickets.

## Development Workflow
- Follow the feature roadmap defined in `docs/implementation_plan.md` unless requirements shift.
- Ensure new endpoints, pages, or models include corresponding documentation updates.
- Maintain auditability by noting significant design decisions in commit messages and documentation.

## Documentation References
- Backend architecture, extensions, and blueprint usage are described in `docs/backend_architecture.md`.
- Development environment setup steps and required tooling are detailed in `docs/development_environment.md`.
- Update this section whenever new authoritative documentation is added so future requests can find the relevant instructions quickly.

## Communication
- Summaries and PR descriptions should clearly state affected areas, testing performed, and any follow-up actions required.
