# ROADMAP_TODO.md

# Website Revision Tracking & Client Approval System — Production Roadmap

**Status:** Planned, unchecked tasks are not implemented.  
**Source:** `production.md` (existing specification); this roadmap deliberately treats the product as a real production application, not an academic submission.  
**Architecture:** Django modular monolith + Django REST Framework + server-rendered Django templates + vanilla JS + same-origin session authentication.  
**Release target:** A secure, monitored, backed-up v1.0 that an agency and its clients can use.

## Operating rules

- Mark a task complete only after its acceptance criteria and relevant tests pass. Use `[x]` and link a PR or commit.
- Build features vertically (model → service → API → permission tests → UI), not by creating hundreds of empty files.
- All business permissions and approval checks run server-side. Frontend restrictions are convenience, not security.
- Keep the original specification authoritative for domain details; record deviations in `DECISIONS.md`.
- Do not add React, microservices, payments, auto-screenshot comparison, or multi-reviewer approvals to v1 without explicit scope change.
- Before deployment, choose the actual host and database; SQLite is for local development, not the default production recommendation.

## Milestone summary

| Milestone       | Phases | Exit criterion                                            |
| --------------- | ------ | --------------------------------------------------------- |
| Foundation      | 00–03  | Requirements, runnable repo, CI, schema and migrations    |
| Core backend    | 04–08  | Secure end-to-end approval workflow and API tests         |
| Product UX      | 09–10  | Staff and client can finish all workflows in browser      |
| Release quality | 11–12  | Tests, security, backup, observability and runbooks       |
| Launch          | 13–15  | Staging UAT, production release, smoke tests and handover |

## Definition of Done (applies to every feature)

- [ ] User story and acceptance criteria documented
- [ ] Data constraints, permissions and validation implemented
- [ ] API behavior documented and tested (where applicable)
- [ ] Frontend handles loading, empty, error and success states (where applicable)
- [ ] Unit/integration/permission tests pass
- [ ] No secrets, debug output, or unintended data exposure
- [ ] Code reviewed, CI green, documentation updated

---

## Phase 00: Product decisions and scope

**Exit:** Deliverable: approved requirements baseline.

- [ ] **00.01** Define target users: agency staff, assigned client reviewer, administrator.
- [ ] **00.02** Document problem, value proposition, primary user journeys and acceptance criteria.
- [ ] **00.03** Confirm project lifecycle: create → pages → round → feedback → resolve/reopen → approve → next round.
- [ ] **00.04** Confirm one assigned client reviewer and at most one open revision round per project.
- [ ] **00.05** Decide whether staff may cancel draft rounds and how abandoned rounds are handled.
- [ ] **00.06** Define immutable history and what happens when project/page/client changes.
- [ ] **00.07** Document non-goals: website hosting, code editing, screenshot archiving, billing, multiple approvers.
- [ ] **00.08** Define MVP versus later releases; record open questions in DECISIONS.md.
- [ ] **00.09** Write user stories and measurable success criteria.
- [ ] **00.10** Create traceability matrix from requirement to endpoint, screen and test.

**Phase gate:** Do not proceed until the exit deliverable is verified and relevant automated checks pass.

## Phase 01: Architecture and engineering design

**Exit:** Deliverable: architecture decision records and diagrams.

- [ ] **01.01** Choose modular Django monolith, DRF same-origin JSON APIs, Django templates and vanilla JS.
- [ ] **01.02** Select supported Python/Django/DRF versions and lock dependencies after compatibility checks.
- [ ] **01.03** Choose PostgreSQL for production (recommended) or MySQL with documented compatibility; SQLite permitted locally.
- [ ] **01.04** Choose session authentication + CSRF, not JWT for same-origin app.
- [ ] **01.05** Define Django apps: accounts, projects, reviews, dashboard; avoid apps per table.
- [ ] **01.06** Draw context, component, request flow, ER and state transition diagrams.
- [ ] **01.07** Define role/ownership permission matrix and object-level authorization.
- [ ] **01.08** Define API v1 URL conventions, pagination, filtering, errors, timestamps and validation response format.
- [ ] **01.09** Decide data retention, attachment policy (none in MVP), privacy and audit requirements.
- [ ] **01.10** Define deployment target, domain, HTTPS, database and media/static strategy.
- [ ] **01.11** Record decisions as ADRs and update production.md if decisions change.

**Phase gate:** Do not proceed until the exit deliverable is verified and relevant automated checks pass.

## Phase 02: Repository and local setup

**Exit:** Deliverable: reproducible clean checkout.

- [ ] **02.01** Create GitHub repository with protected main branch and feature branch conventions.
- [ ] **02.02** Create .gitignore for .venv, .env, SQLite, cache, logs, uploads and secrets.
- [ ] **02.03** Create README, ROADMAP_TODO.md, production.md, DECISIONS.md, CHANGELOG.md.
- [ ] **02.04** Create Python virtual environment and configure VS Code interpreter.
- [ ] **02.05** Install Django, DRF, database driver, environment loader, test/lint/security tools.
- [ ] **02.06** Create requirements.in/requirements.txt or pyproject with pinned dependencies.
- [ ] **02.07** Start Django project config and apps; configure INSTALLED_APPS.
- [ ] **02.08** Split settings by environment only if needed; use environment variables for secrets.
- [ ] **02.09** Configure timezone, language, logging and static/media paths.
- [ ] **02.10** Run initial migrate, check, runserver and verify admin loads.
- [ ] **02.11** Add formatting/linting (Ruff), pre-commit hooks and basic test command.
- [ ] **02.12** Set up GitHub Actions to run lint, checks and tests on push/PR.
- [ ] **02.13** Verify a second clean environment can install and start the app.

**Phase gate:** Do not proceed until the exit deliverable is verified and relevant automated checks pass.

## Phase 03: Database and domain modeling

**Exit:** Deliverable: reviewed migrations and ERD.

- [ ] **03.01** Define custom User model before first application migrations; email uniqueness and role rules.
- [ ] **03.02** Define Project with assigned client, creator, metadata and lifecycle fields.
- [ ] **03.03** Define ProjectPage with ordering, labels, ownership and archival rules.
- [ ] **03.04** Define RevisionRound with project, sequence number, status and timestamps.
- [ ] **03.05** Define RoundPage with unique (round,page) and snapshot label/preview URL.
- [ ] **03.06** Define Feedback with round page, author, body and open/resolved/reopened status.
- [ ] **03.07** Define append-only FeedbackEvent with actor, action, note and timestamps.
- [ ] **03.08** Define Approval with one-to-one round, approving reviewer, note and timestamp.
- [ ] **03.09** Specify FK on_delete behaviors to protect history.
- [ ] **03.10** Add constraints for unique sequence numbers, round-page pairing and approval uniqueness.
- [ ] **03.11** Enforce one open round per project with transaction/locking strategy compatible with chosen DB.
- [ ] **03.12** Add indexes for client project list, rounds, feedback status and event timeline.
- [ ] **03.13** Write migrations and run migrate from blank database.
- [ ] **03.14** Build model factories/fixtures and test constraints, cross-project references and deletion rules.
- [ ] **03.15** Document database backup and migration rollback approach.

**Phase gate:** Do not proceed until the exit deliverable is verified and relevant automated checks pass.

## Phase 04: Accounts, sessions and permissions

**Exit:** Deliverable: secure role-aware authentication.

- [ ] **04.01** Implement admin-provisioned accounts; no public signup in MVP.
- [ ] **04.02** Implement login, logout POST, password hashing and session expiration.
- [ ] **04.03** Implement password reset via configured email service or documented admin reset flow.
- [ ] **04.04** Implement staff/client role checks with least privilege.
- [ ] **04.05** Enforce object-level checks on every project, round, page and feedback query.
- [ ] **04.06** Restrict Django Admin access to trusted staff; avoid using superuser to bypass approval workflow.
- [ ] **04.07** Configure CSRF, secure cookies, password validators and brute-force throttling.
- [ ] **04.08** Implement /api/v1/me/ and safe frontend session handling.
- [ ] **04.09** Test anonymous, staff, assigned client, unrelated client and disabled account scenarios.
- [ ] **04.10** Verify ID guessing cannot expose other clients’ projects or histories.

**Phase gate:** Do not proceed until the exit deliverable is verified and relevant automated checks pass.

## Phase 05: Projects and website pages

**Exit:** Deliverable: staff CRUD + client read-only access.

- [ ] **05.01** Implement project creation, edit, list, detail and controlled archive actions.
- [ ] **05.02** Assign one active reviewer to a project and validate account role.
- [ ] **05.03** Implement project page create, edit, reorder and archive.
- [ ] **05.04** Block unsafe deletion of projects/pages referenced by historical rounds.
- [ ] **05.05** Create serializers with field-level validation and server-owned fields read-only.
- [ ] **05.06** Create DRF endpoints, pagination, search and status filters.
- [ ] **05.07** Build staff project list, create/edit form and project detail UI.
- [ ] **05.08** Build client project list filtered by ownership.
- [ ] **05.09** Handle empty states, form errors, unauthorized and not-found responses.
- [ ] **05.10** Write unit/API tests for CRUD, validation, ownership and historical integrity.

**Phase gate:** Do not proceed until the exit deliverable is verified and relevant automated checks pass.

## Phase 06: Revision rounds and preview snapshots

**Exit:** Deliverable: client-visible review rounds.

- [ ] **06.01** Define draft/open/approved lifecycle exactly and allowed transitions.
- [ ] **06.02** Implement atomic per-project sequential round numbering.
- [ ] **06.03** Implement create draft round and add selected project pages.
- [ ] **06.04** Validate preview URLs (http/https only), limits and unsafe schemes.
- [ ] **06.05** Snapshot page name and preview URL at round publication.
- [ ] **06.06** Publish/open round only when required page previews are complete.
- [ ] **06.07** Prevent opening second round while one is active, including concurrent requests.
- [ ] **06.08** Lock published snapshot fields according to documented policy.
- [ ] **06.09** Build staff round creation, preview entry and publish screens.
- [ ] **06.10** Build client round detail and external preview links with clear external-site warning.
- [ ] **06.11** Test cross-project pages, empty rounds, concurrent publishing and historical snapshots.

**Phase gate:** Do not proceed until the exit deliverable is verified and relevant automated checks pass.

## Phase 07: Feedback and immutable event history

**Exit:** Deliverable: complete feedback lifecycle.

- [ ] **07.01** Implement assigned client feedback submission for an open round page.
- [ ] **07.02** Validate nonblank content, maximum length, HTML escaping and ownership.
- [ ] **07.03** Implement staff resolve action with resolution note.
- [ ] **07.04** Implement client reopen action with reason.
- [ ] **07.05** Record created/resolved/reopened events in the same transaction as state changes.
- [ ] **07.06** Prevent editing/deleting event history through normal APIs.
- [ ] **07.07** Block feedback mutations after approval.
- [ ] **07.08** Expose feedback lists, filters, details and chronological history API.
- [ ] **07.09** Build comment composer, feedback cards, status filters and timeline UI.
- [ ] **07.10** Test all transitions, role boundaries, race conditions and duplicate requests.

**Phase gate:** Do not proceed until the exit deliverable is verified and relevant automated checks pass.

## Phase 08: Approval workflow and audit

**Exit:** Deliverable: correct formal approval record.

- [ ] **08.01** Define exact approval eligibility: assigned client, open round, no unresolved feedback.
- [ ] **08.02** Implement approval service using transaction.atomic and row locks where supported.
- [ ] **08.03** Recheck unresolved feedback inside the transaction before approval.
- [ ] **08.04** Create one-to-one approval record and change round status atomically.
- [ ] **08.05** Prevent duplicate approvals and simultaneous feedback/approval race conditions.
- [ ] **08.06** Make approved round and related review records read-only.
- [ ] **08.07** Show approval confirmation, timestamp, reviewer and optional note.
- [ ] **08.08** Provide approved-round history view and audit timeline.
- [ ] **08.09** Test open feedback rejection, reopened rejection, unauthorized approval and concurrency.
- [ ] **08.10** Test creating the next round without modifying earlier approvals.

**Phase gate:** Do not proceed until the exit deliverable is verified and relevant automated checks pass.

## Phase 09: Frontend UI and accessibility

**Exit:** Deliverable: complete responsive user journeys.

- [ ] **09.01** Define design tokens, typography, spacing, colors, components and layout.
- [ ] **09.02** Create base template, navigation, flash messages and role-aware menus.
- [ ] **09.03** Build login, reset flow and unauthorized/not-found/error pages.
- [ ] **09.04** Build staff dashboard with project and review status summaries.
- [ ] **09.05** Build staff project list/detail/forms and page management.
- [ ] **09.06** Build staff revision round creation and feedback resolution screens.
- [ ] **09.07** Build client dashboard, project detail, round detail and feedback forms.
- [ ] **09.08** Build client approval confirmation and historical approvals view.
- [ ] **09.09** Create shared fetch wrapper with CSRF, JSON errors and session-expired handling.
- [ ] **09.10** Add loading, success, error, empty and retry states; avoid duplicate submissions.
- [ ] **09.11** Ensure mobile/tablet/desktop responsiveness and keyboard accessibility.
- [ ] **09.12** Add accessible labels, focus states, semantic headings and contrast checks.
- [ ] **09.13** Test with real browsers, not just responsive emulator.

**Phase gate:** Do not proceed until the exit deliverable is verified and relevant automated checks pass.

## Phase 10: Reporting and operational features

**Exit:** Deliverable: trustworthy dashboard metrics.

- [ ] **10.01** Define dashboard metrics precisely: projects, open rounds, unresolved feedback, approvals.
- [ ] **10.02** Implement permission-filtered aggregate queries.
- [ ] **10.03** Build staff overview and client-specific summary widgets.
- [ ] **10.04** Implement project revision timeline and feedback status summaries.
- [ ] **10.05** Implement pagination and filtering for historical records.
- [ ] **10.06** Document date/time display and timezone behavior.
- [ ] **10.07** Add structured application logging with request IDs if feasible.
- [ ] **10.08** Ensure no secrets or sensitive client content enter logs.

**Phase gate:** Do not proceed until the exit deliverable is verified and relevant automated checks pass.

## Phase 11: Automated tests and quality gates

**Exit:** Deliverable: passing CI and release candidate.

- [ ] **11.01** Write model tests for constraints, relationships and state rules.
- [ ] **11.02** Write service tests for round creation, feedback transitions and approval.
- [ ] **11.03** Write API tests for success and validation failure cases.
- [ ] **11.04** Build complete role × endpoint permission matrix tests.
- [ ] **11.05** Write concurrency tests for two round openings and approval vs feedback.
- [ ] **11.06** Test CSRF, XSS output escaping, unsafe URL schemes and file handling (if added).
- [ ] **11.07** Test migrations on empty DB and on populated staging data.
- [ ] **11.08** Run lint/format checks and Django system/deploy checks.
- [ ] **11.09** Run dependency vulnerability scan and secret scan.
- [ ] **11.10** Add integration tests for staff and client end-to-end flows.
- [ ] **11.11** Run accessibility and responsive manual checks.
- [ ] **11.12** Test slow networks, stale sessions, duplicate clicks and error pages.
- [ ] **11.13** Measure slow DB queries and add indexes only when justified.
- [ ] **11.14** Require CI green before merge and tag release candidate.

**Phase gate:** Do not proceed until the exit deliverable is verified and relevant automated checks pass.

## Phase 12: Production hardening

**Exit:** Deliverable: secure deployable build.

- [ ] **12.01** Set DEBUG=False, environment-specific SECRET_KEY and strict ALLOWED_HOSTS.
- [ ] **12.02** Configure HTTPS redirect, HSTS after verification, secure cookies and CSRF trusted origins.
- [ ] **12.03** Configure production DB credentials with minimum privileges.
- [ ] **12.04** Configure static assets collection and web server static serving.
- [ ] **12.05** Choose persistent media storage only if uploads are in scope.
- [ ] **12.06** Configure SMTP provider for password reset and notification emails if implemented.
- [ ] **12.07** Configure CORS only if cross-origin clients truly exist.
- [ ] **12.08** Set application timeouts, body size limits and sensible rate limits.
- [ ] **12.09** Implement database backups, retention, encrypted storage and restore rehearsal.
- [ ] **12.10** Configure structured logs, error monitoring, health endpoint and uptime alerts.
- [ ] **12.11** Document secret rotation, admin access and dependency patch process.
- [ ] **12.12** Write deployment and rollback runbooks.

**Phase gate:** Do not proceed until the exit deliverable is verified and relevant automated checks pass.

## Phase 13: Staging deployment and UAT

**Exit:** Deliverable: approved staging release.

- [ ] **13.01** Provision staging server/app host, database and staging domain.
- [ ] **13.02** Set environment variables and deploy from tagged commit.
- [ ] **13.03** Run migrations and collectstatic via repeatable release command.
- [ ] **13.04** Create test staff and client accounts with non-sensitive demo data.
- [ ] **13.05** Verify login, CSRF, session, permissions and external preview links.
- [ ] **13.06** Run end-to-end acceptance scenarios in real browsers.
- [ ] **13.07** Test backup restore and a migration rollback on staging.
- [ ] **13.08** Run load smoke tests for expected small-team traffic.
- [ ] **13.09** Resolve blocking bugs and update CHANGELOG/release notes.
- [ ] **13.10** Freeze release candidate and record go/no-go checklist.

**Phase gate:** Do not proceed until the exit deliverable is verified and relevant automated checks pass.

## Phase 14: Production deployment

**Exit:** Deliverable: live HTTPS application.

- [ ] **14.01** Choose host supporting Django ASGI/WSGI; do not assume PHP-only cPanel is sufficient.
- [ ] **14.02** Provision production DB, app runtime, domain DNS and TLS certificate.
- [ ] **14.03** Create secrets in host secret manager or protected environment.
- [ ] **14.04** Set up production process manager/application server and reverse proxy as needed.
- [ ] **14.05** Configure static serving and persistent storage paths.
- [ ] **14.06** Take pre-release DB backup and verify restore instructions.
- [ ] **14.07** Deploy tagged build, install pinned dependencies and run migrate.
- [ ] **14.08** Run collectstatic and start/reload app with health checks.
- [ ] **14.09** Create first admin through secure procedure; disable debug and sample data.
- [ ] **14.10** Verify HTTPS, login/logout, permissions, project creation, review and approval.
- [ ] **14.11** Inspect error logs, DB connectivity, static assets and outbound email.
- [ ] **14.12** Record release version, deployment timestamp and rollback reference.

**Phase gate:** Do not proceed until the exit deliverable is verified and relevant automated checks pass.

## Phase 15: Post-deployment verification and handover

**Exit:** Deliverable: maintainable production service.

- [ ] **15.01** Run production smoke test with staff and client test accounts.
- [ ] **15.02** Verify backups execute and test a restore to an isolated environment.
- [ ] **15.03** Set monitoring alerts and document escalation/incident contacts.
- [ ] **15.04** Confirm permissions and audit history with realistic sample workflow.
- [ ] **15.05** Document admin onboarding, account provisioning and recovery.
- [ ] **15.06** Document routine updates, migrations, backups and secret rotation.
- [ ] **15.07** Set maintenance cadence for dependencies and security patches.
- [ ] **15.08** Document known limitations, support process and change request workflow.
- [ ] **15.09** Create v1.0 release notes and archive architecture decisions.
- [ ] **15.10** Move optional features into a separately prioritized backlog.

**Phase gate:** Do not proceed until the exit deliverable is verified and relevant automated checks pass.

---

## End-to-end production acceptance scenarios

- [ ] Staff creates client account, project and pages; client sees only assigned project.
- [ ] Staff opens round 1 with preview snapshots; client views every page and submits feedback.
- [ ] Staff resolves an issue; client reopens it; full event history remains intact.
- [ ] Approval is rejected while any feedback is open or reopened.
- [ ] Client approves after all feedback is resolved; exact round and reviewer are recorded.
- [ ] Round 1 is immutable after approval; round 2 can be created independently.
- [ ] Unrelated clients cannot retrieve, mutate or approve another client's data, even with guessed IDs.
- [ ] Two simultaneous publish/approval requests do not create duplicate rounds or approvals.
- [ ] Browser refresh, expired session, invalid form, mobile layout and external link failure are handled gracefully.
- [ ] New deployment survives restart, serves static files, logs errors and can restore from backup.

## Optional post-v1 backlog (not release blockers)

- [ ] Email notifications and digests beyond essential password reset
- [ ] Multiple client reviewers and configurable approval policy
- [ ] File attachments, screenshots and annotation tools with secure storage
- [ ] Automated website snapshots/diffing and preview archival
- [ ] Webhooks, third-party integrations and public API tokens
- [ ] Advanced search, export formats and richer analytics
- [ ] Multi-tenant agencies, subscription billing and quotas
- [ ] Async job queue/caching only when measured demand warrants it

## Execution cadence

For each numbered task: implement a small vertical slice, run tests, commit, and update the checkbox. At the end of each phase, record evidence (tests, screenshots, API examples, migrations, staging link) in the PR or release notes. Do not claim production-ready status before Phase 15.
