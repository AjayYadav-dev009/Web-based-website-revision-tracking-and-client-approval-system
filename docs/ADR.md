# Architecture Decision Records (ADRs)

**Product:** Website Revision Tracking and Client Approval System  
**Status:** Proposed decisions for review | **Updated:** 2026-11-17

An ADR records the problem, options, choice, reasons, consequences and circumstances that would justify revisiting the choice. Accepted decisions should not be silently rewritten; create a superseding ADR when direction changes.

## ADR-001 — Modular monolith rather than microservices
**Status:** Proposed

**Context:** A small development team is building one coherent workflow with shared transactions and tightly related data.

**Decision:** One Django deployable application, split into domain apps (`accounts`, `projects`, `reviews`, `dashboard`) with explicit module boundaries.

**Alternatives:** Unstructured monolith; microservices.

**Why:** Simpler local development, deployment, transactions, observability and testing; domain separation without network overhead.

**Consequences:** All modules share a deployment and database; discipline is needed to avoid cross-module coupling. Revisit only if independent scaling/team ownership becomes a measured need.

## ADR-002 — Django + Django REST Framework
**Status:** Proposed

**Context:** Product requires authentication, relational data, role-based workflows and JSON endpoints.

**Decision:** Django for ORM, auth, admin and templates; DRF for API serializers, views, permissions and pagination.

**Alternatives:** Flask/FastAPI, Laravel, fully server-rendered Django without DRF.

**Why:** Strong integrated platform, mature security defaults, admin tooling and a clear path to API clients. DRF is justified by frontend API interactions, not by a requirement for a separate frontend deployment.

**Consequences:** API layer and serializers add complexity. Keep business rules in domain services/models and avoid duplicate logic in templates and API views.

## ADR-003 — Django templates + vanilla JavaScript
**Status:** Proposed

**Context:** Dashboard screens require forms, lists and async feedback actions, not a highly interactive SPA.

**Decision:** Render page shells through Django templates; use `fetch()` against same-origin JSON endpoints for dynamic actions.

**Alternatives:** React/Next.js SPA; fully server-rendered forms.

**Why:** Smaller build/deployment surface and faster delivery using existing skills.

**Consequences:** Frontend state and DOM updates must be handled carefully. Revisit if UI complexity grows enough to justify a component framework.

## ADR-004 — Session authentication and CSRF
**Status:** Proposed

**Context:** Browser-based app and API share the same origin.

**Decision:** Django session cookies, standard password hashing and CSRF protection on unsafe requests. Use secure/HttpOnly/SameSite cookies in production as appropriate.

**Alternatives:** JWT access/refresh tokens; third-party identity provider.

**Why:** Native fit for same-origin browser clients, with fewer token storage/rotation pitfalls.

**Consequences:** Frontend must send CSRF tokens and credentials correctly. JWT may be reconsidered if independent mobile or third-party clients become a real requirement.

## ADR-005 — Custom user model from day one
**Status:** Proposed — must settle before initial migrations

**Context:** Need staff/client business roles and may expand identity fields later.

**Decision:** `accounts.User(AbstractUser)` with explicit `role` (`staff`, `client`); set `AUTH_USER_MODEL` before first migration. Keep Django `is_staff` (admin access) distinct from business `role`.

**Alternatives:** Default User + profile; Groups-only roles.

**Why:** Avoid costly later user-model swap; simple MVP authorization model.

**Consequences:** Permissions must use business role and object assignment, not `is_staff` alone. Choose one authoritative role model and test it.

## ADR-006 — SQLite locally, MySQL in production
**Status:** Proposed, production provider undecided

**Context:** Fast setup is desirable, but production needs robust concurrency and operational backups.

**Decision:** SQLite may be used for initial local development; MySQL is the planned production relational database. CI/staging must run integration tests against the production database engine before release.

**Alternatives:** MySQL everywhere; PostgreSQL everywhere.

**Why:** Fits existing MySQL familiarity while allowing a lightweight start.

**Consequences:** SQLite differs from MySQL in locking, constraints and SQL behavior. **Do not assume partial unique indexes work identically on MySQL.** Protect one-open-round invariants using transactional parent-row locking, checks and production-database tests. Consider MySQL locally if consistency is more important than convenience.

## ADR-007 — Revision snapshot records, not website archiving
**Status:** Proposed

**Context:** Need historical review context without hosting or copying client sites.

**Decision:** `RoundPage` stores immutable page label, slug and preview URL snapshot at publication. External website content is not captured.

**Alternatives:** Live page references only; screenshot/archive service.

**Why:** Low complexity and clear version-to-feedback linkage.

**Consequences:** A preview URL may later show changed content. UI and documentation must disclose this limitation. Actual visual evidence preservation is a separate future feature.

## ADR-008 — Approval transaction and immutable audit events
**Status:** Proposed

**Context:** Approval must be trustworthy as an application workflow, including concurrent requests.

**Decision:** Approval service validates assigned client, round state and all feedback within an atomic transaction; locks appropriate records, creates one Approval row, and updates round status. Feedback events are append-only. Approved records are read-only through normal application paths.

**Alternatives:** Client-side validation; view-only checks; mutable audit history.

**Why:** Centralizes invariants and prevents inconsistent approval states.

**Consequences:** More backend tests and careful transaction design required. Database administrators still have privileged write access, so this is not a cryptographic or legally certified audit system.

## ADR-009 — Domain-oriented Django apps and services
**Status:** Proposed

**Context:** Authentication, projects and review workflow have different responsibilities.

**Decision:** Apps: `accounts`, `projects`, `reviews`, `dashboard`. Models own persistence shape; serializers validate API input/output; views coordinate HTTP; permissions enforce access; services handle multi-step state changes.

**Alternatives:** One app for everything; app per model; heavyweight clean-architecture abstraction layers.

**Why:** Maintainable boundaries without excessive scaffolding.

**Consequences:** Avoid circular imports and duplicated rules. Create service modules where workflows warrant them, not for trivial CRUD.

## ADR-010 — Production operations and release process
**Status:** Proposed

**Context:** Application handles client review records and must be recoverable.

**Decision:** Environment-driven settings, secrets outside Git, HTTPS, reverse proxy and production WSGI/ASGI server, managed database where feasible, static-file collection, structured logs, automated tests, staging verification, migration and rollback plan, scheduled backups with tested restore.

**Alternatives:** Development server on public internet; manual-only release without staging.

**Why:** Security and recoverability are part of product correctness.

**Consequences:** Hosting selection and operational budget remain open. Never deploy Django `runserver` as the production web server.

## Decision log and review gates
| ADR | Status | Must confirm before |
|---|---|---|
| 001–003 | Proposed | Architecture implementation |
| 004–005 | Proposed | First authentication migration |
| 006 | Proposed | Database setup and deployment selection |
| 007–009 | Proposed | Revision/approval workflow implementation |
| 010 | Proposed | Staging and production launch |

## Open questions
- Final hosting/database provider and whether MySQL is mandatory.
- Client reassignment, zero-feedback approval, approved-round revocation and page inclusion rules.
- Retention period, backup frequency and restoration targets.
- Need for invitations/email or only manually created client accounts.

## Change process
When an architectural choice changes, add `ADR-011`, etc., with the new decision and mark the previous ADR `Superseded by ADR-XXX`. Preserve the reasoning history.
