# Product Requirements Document (PRD)

**Product:** Website Revision Tracking and Client Approval System  
**Version:** 1.0 draft | **Status:** Proposed, pending product decisions | **Updated:** 2026-11-17  
**Owner:** Product owner (to confirm) | **Audience:** Developers, reviewers, stakeholders

## 1. Executive summary
A browser-based workspace where an agency manages website projects, creates revision rounds with page-specific preview links, collects client feedback, records issue resolution and reopening, and obtains explicit approval for a specific revision round. It provides a clear review history instead of scattered chat/email messages.

**Important boundary:** A preview URL is a recorded link, not an archived copy of the website. The external website can change after approval.

## 2. Problem and opportunity
Agency website review processes often mix chat, calls, email and spreadsheets. Feedback loses its page/version context; resolution status becomes ambiguous; approvals are hard to attribute to a specific revision. A centralized system should improve traceability and accountability without requiring a website builder or Git integration.

## 3. Users and jobs to be done
| Persona | Job | Primary needs |
|---|---|---|
| Agency staff | Organize work and request review | Create projects/pages/rounds; publish previews; resolve issues; view history |
| Assigned client reviewer | Review and approve work | Access only own projects; see page previews; leave/reopen feedback; approve a round |
| Operational administrator | Maintain application | Provision accounts, troubleshoot through Django Admin; cannot forge client approval via normal API |

**Initial access model:** Multiple agency staff may work on projects; each project has one designated client reviewer. One open revision round per project.

## 4. Product goals
1. Centralize project, page, revision and feedback records.
2. Make review and approval attributable to a specific user and revision.
3. Prevent cross-client data access and unauthorized workflow changes.
4. Keep approved history read-only in normal application workflows.
5. Deliver understandable staff and client interfaces, backed by testable APIs.

## 5. Success measures and acceptance targets
- 100% of core workflow actions are associated with an authenticated actor.
- A client cannot read or modify another client's project (verified by automated tests).
- A round with any `open` or `reopened` feedback cannot be approved.
- One successful approval yields one Approval record with actor and server timestamp.
- A new revision does not change earlier approved rounds.
- All release-blocking security and workflow tests pass before production deployment.
- Usability: staff and client can complete an end-to-end review without administrator intervention, after accounts are provisioned.

These are **release acceptance targets**, not observed metrics.

## 6. Primary workflows
### A. Create a project
Staff signs in → creates project → selects client → creates website pages → project appears in authorized dashboards.

### B. Prepare and publish revision
Staff creates draft revision round → adds page snapshots with preview URLs → validates required pages and URLs → publishes the round → assigned client can review it.

### C. Submit and resolve feedback
Client opens current round → selects page → submits comment → system records `open` feedback and an event → staff records a resolution note → feedback becomes `resolved` → client may reopen with a reason → staff resolves again.

### D. Approve
Assigned client requests approval → backend locks/rechecks current round and feedback → blocks if any unresolved issue remains → creates unique approval record and marks round approved in one transaction → historical records become read-only → staff may prepare/publish next round.

### E. Review history
Authorized users can inspect prior rounds, page links as recorded, feedback events, approval actor and timestamp.

## 7. Functional requirements
| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Authenticate users with secure login/logout | Must |
| FR-02 | Enforce staff/client roles and per-project access | Must |
| FR-03 | Provision users through Django Admin | Must |
| FR-04 | Staff create, edit, list and view projects | Must |
| FR-05 | Staff assign one client reviewer to each project | Must |
| FR-06 | Staff manage ordered project pages; retain historical references | Must |
| FR-07 | Staff create numbered draft revision rounds | Must |
| FR-08 | Staff add round-page snapshots and valid preview URLs | Must |
| FR-09 | Staff publish a valid draft; enforce one open round | Must |
| FR-10 | Client sees only assigned projects and published rounds | Must |
| FR-11 | Client submits page-specific feedback in open round | Must |
| FR-12 | Staff resolves feedback with nonempty resolution note | Must |
| FR-13 | Client reopens resolved feedback with nonempty reason | Must |
| FR-14 | System records append-only feedback status events | Must |
| FR-15 | Assigned client approves eligible open round | Must |
| FR-16 | Approval blocks on unresolved feedback and duplicate requests | Must |
| FR-17 | Approved rounds and related review records are read-only | Must |
| FR-18 | Staff and client dashboards show authorized counts and activity | Must |
| FR-19 | Project history shows revisions, feedback and approvals | Must |
| FR-20 | Friendly validation, empty, loading and error states | Must |
| FR-21 | Responsive and keyboard-accessible UI | Must |
| FR-22 | Optional feedback attachments | Later |
| FR-23 | Email notifications/invitations | Later |
| FR-24 | CSV/PDF export and richer filtering | Later |

## 8. Nonfunctional requirements
**Security:** HTTPS in production; secure session cookies; CSRF for state-changing browser requests; password hashing; object-level authorization; no secrets in Git; rate limiting on authentication at reverse proxy or app layer; safe redirects; output escaping; URL validation and safe external-link behavior.

**Reliability:** Atomic approval transactions; uniqueness constraints; concurrency-safe round publishing; backup/restore process; structured error logging.

**Performance:** Paginate lists, index common filters, avoid N+1 queries, measure response times with realistic seed data before setting numerical service targets.

**Maintainability:** Django apps by domain, tests for workflows, documented migrations, pinned dependencies, environment-driven configuration, linting/formatting.

**Accessibility:** Labeled forms, visible focus, keyboard navigation, meaningful error messages, adequate contrast and mobile usability.

**Privacy:** Minimize personal data; restrict client access; document retention and deletion policy before launch. Admin access is privileged and must be controlled.

## 9. UX / screen inventory
- Login/logout and access-denied/error pages.
- Staff dashboard; project list/create/edit/detail; project pages manager; round draft editor/publish; open round feedback management; approval/history views.
- Client dashboard; project detail; revision page previews and feedback; reopen/approval confirmation; read-only history.
- Shared responsive navigation, notifications/toasts, form validation and empty states.

## 10. Data entities
`User`, `Project`, `ProjectPage`, `RevisionRound`, `RoundPage`, `Feedback`, `FeedbackEvent`, `Approval`. See `production.md` for the proposed field-level schema. The user model must be selected before initial Django migrations.

## 11. Dependencies and constraints
- Django + Django REST Framework backend, Django templates and vanilla JS frontend.
- Same-origin session authentication; JSON API for application actions.
- Local SQLite for early development is acceptable; MySQL is the proposed production database, with production parity testing required.
- External preview sites are outside our control and may require their own access permissions.
- No claim of legal electronic signature, certified audit trail or preserved website snapshot.

## 12. Risks and mitigations
| Risk | Mitigation |
|---|---|
| Preview link changes after approval | Clearly disclose link-only archival; optionally add true snapshot service in future |
| Cross-tenant data leak | Scoped querysets + object permission tests |
| Concurrent publish/approval requests | Transactions, locks, database constraints and tests |
| Client confusion about status | Explicit labels, timeline and confirmation UI |
| Scope creep | Freeze v1.0 scope; defer enhancements |
| SQLite/MySQL differences | Test migrations and constraints on production database before launch |
| Operational data loss | Tested backups and restoration drills |

## 13. Release acceptance
Release requires all Must requirements implemented and verified, critical test suite passing, security review, migration verification, staging end-to-end demonstration, backup/restore rehearsal, and deployment smoke tests. See `ROADMAP_TODO.md`.

## 14. Open product decisions
1. Can an agency staff member reassign a project to a different client after reviews exist? Recommended: prohibit silently changing historical reviewer; require controlled reassignment and audit.
2. Must every revision include **all** project pages or only selected changed pages? Recommended: selected pages allowed, with at least one page per round.
3. Is client approval allowed when no feedback was ever submitted? Recommended: yes, after explicit confirmation.
4. Should an approved round ever be revoked? Recommended: no in v1; create a new round instead.
5. Will staff provision clients manually or should invitations/reset email be in v1? Recommended: manual provisioning initially.
6. Which production hosting and database provider will be used? Pending selection.
7. What is the retention/deletion policy for client/project data? Pending policy decision.

## 15. Related documents
- `FEATURE_SCOPE.md`: release boundary and feature priorities.
- `BUSINESS_RULES_ACCEPTANCE.md`: enforceable behavior and test scenarios.
- `ADR.md`: architecture decisions and consequences.
- `production.md`: detailed technical blueprint.
- `ROADMAP_TODO.md`: implementation tasks and release gates.
