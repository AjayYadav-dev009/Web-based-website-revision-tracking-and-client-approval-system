# Feature Scope — v1.0

**Status:** Proposed | **Updated:** 2026-11-17

## Product boundary
A browser-based website review coordination and approval tool. It records review metadata and external preview links. It does **not** host or archive website versions.

## Must-have (v1.0 release blockers)
- [ ] Secure session login/logout, staff/client business roles and object-level permissions.
- [ ] User provisioning through Django Admin.
- [ ] Project CRUD and assignment to one designated client reviewer.
- [ ] Project-page creation, ordering, editing and deactivation.
- [ ] Sequential draft revision rounds and page-specific preview URL snapshots.
- [ ] Round publishing, one open round per project, no modification of published snapshots.
- [ ] Client project/round/page review interface.
- [ ] Page-specific client feedback submission.
- [ ] Staff resolution notes and client reopening reasons.
- [ ] Append-only feedback event history.
- [ ] Client approval of eligible open round, unique approval record and server timestamp.
- [ ] Read-only approved review history; no silent retroactive changes.
- [ ] Role-specific dashboards and basic project history/reporting.
- [ ] Responsive, accessible forms with validation/error/empty/loading states.
- [ ] Automated authorization, workflow, concurrency and API tests.
- [ ] Staging, secure deployment, backups, restore test and release smoke checks.

## Should-have (include if feasible without delaying core release)
- [ ] Basic server-side search/filter and pagination.
- [ ] Useful status badges and timeline summaries.
- [ ] Seed/demo data command for non-production environments.
- [ ] Simple admin-friendly account management documentation.

## Could-have (post-v1 backlog)
- [ ] Feedback screenshot/image attachments with secure upload and retention rules.
- [ ] Email invitation, password reset and workflow notifications.
- [ ] CSV/PDF exports of review history.
- [ ] Preview URL availability monitoring.
- [ ] More granular agency staff roles and project assignments.
- [ ] Enhanced analytics, saved filters, accessibility refinements beyond baseline.
- [ ] Webhook integrations and optional external issue tracker integration.

## Won't-have in v1.0
- Website editor, page builder or hosting.
- Git repository, CI/CD, deployment or rollback control for client websites.
- Screenshot capture, visual diffing or actual archival of preview site contents.
- Multiple client approvers, voting, quorum or approval chains.
- Multiple open rounds for one project.
- Payments, subscriptions, invoices, contracts or legally certified signatures.
- Native mobile apps, anonymous approval links, real-time chat, WebSockets.
- React/Next.js frontend, microservices, Redis, Celery, Kubernetes by default.
- AI-generated review comments.

## Roles and access boundaries
- **Staff:** Manage projects, pages and rounds; resolve feedback; view history. Cannot approve as the client through normal APIs.
- **Assigned client:** Read only assigned projects; submit/reopen feedback in open rounds; approve eligible round.
- **Other client:** No access to project details, feedback, round pages or approval records.
- **Superuser:** Operational Django Admin access; does not override client approval identity in normal workflow.

## Scope-change policy
1. Write a change request with problem, affected users and desired outcome.
2. Estimate impact on models, API, frontend, tests, security, schedule and migrations.
3. Classify as blocker, v1 enhancement or post-v1.
4. Approve before implementing; update PRD, business rules and roadmap.
5. Avoid shipping partially integrated features just because they are visually impressive.

## Release gate
v1.0 ships only when every Must-have is implemented, tested and documented, no known critical/high security issue remains, staging workflow passes, and recovery/rollback instructions are validated.

## Assumptions to confirm
One client reviewer per project; selected page snapshots per round; manual client account provisioning; approval without feedback permitted; no revocation of approved rounds. Until confirmed, these are proposals rather than final stakeholder-approved policy.
