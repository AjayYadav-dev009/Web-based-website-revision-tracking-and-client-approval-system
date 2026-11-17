# Business Rules and Acceptance Criteria

**Version:** 1.0 draft | **Status:** Proposed | **Updated:** 2026-11-17

## 1. Terms
- **Project:** Client website engagement.
- **ProjectPage:** Logical website page, e.g. Home.
- **RevisionRound:** Numbered review cycle, `draft`, `open`, or `approved`.
- **RoundPage:** Frozen record of a page name, slug and external preview URL for one round.
- **Feedback:** Client's page-specific issue, `open`, `resolved`, or `reopened`.
- **FeedbackEvent:** Append-only transition record with actor and time.
- **Approval:** Unique record proving which assigned client user approved which round and when.

## 2. Authorization rules
| ID | Rule |
|---|---|
| AUTH-01 | All application data endpoints require authentication unless explicitly designated public. |
| AUTH-02 | Staff may manage project, page and round data; client reviewers cannot. |
| AUTH-03 | Client can access only projects where they are the assigned reviewer. |
| AUTH-04 | All nested resources inherit project authorization checks, even when addressed by direct ID. |
| AUTH-05 | Client cannot change role or ownership through API input. |
| AUTH-06 | Only assigned client may create/reopen feedback or approve their project's current open round. |
| AUTH-07 | Staff can resolve feedback but cannot impersonate a client approval. |
| AUTH-08 | Unauthorized access is denied without leaking other-client content. |

## 3. Project and page rules
| ID | Rule |
|---|---|
| PROJ-01 | A project must have a title and a valid client-role reviewer. |
| PROJ-02 | Page slug must be unique within a project. |
| PROJ-03 | A page referenced by historical rounds is deactivated, not destructively deleted. |
| PROJ-04 | Project status is independent of revision approval status. |
| PROJ-05 | Reviewer reassignment after review begins requires explicit policy; never rewrite historic approval actor. |

## 4. Revision round rules
| ID | Rule |
|---|---|
| REV-01 | Round numbers are sequential and unique per project. |
| REV-02 | A new round starts as `draft`. |
| REV-03 | Only staff can publish a draft round. |
| REV-04 | A draft needs at least one valid RoundPage before publishing. |
| REV-05 | A project has at most one `open` round. |
| REV-06 | Publishing freezes page labels, slugs and preview URLs for that round. |
| REV-07 | Only an `open` round can be approved. |
| REV-08 | Approved round is terminal and read-only via normal application operations. |
| REV-09 | A new round never alters an earlier round's snapshots, events or approval. |
| REV-10 | A round page must refer to a ProjectPage belonging to the same project. |

## 5. Feedback rules
| ID | Rule |
|---|---|
| FB-01 | Feedback must reference a RoundPage of an `open` round. |
| FB-02 | Feedback body must be nonempty after trimming and within configured length limit. |
| FB-03 | New feedback starts `open` with a `created` event. |
| FB-04 | Only staff can move `open`/`reopened` to `resolved`; note required. |
| FB-05 | Only assigned client can move `resolved` to `reopened`; reason required. |
| FB-06 | Invalid transitions are rejected without changing stored state. |
| FB-07 | Every accepted transition appends an event with actor, old/new status, note and server time. |
| FB-08 | Events cannot be edited or deleted via normal application APIs. |
| FB-09 | Feedback is immutable once its round is approved. |

## 6. Approval rules
| ID | Rule |
|---|---|
| APP-01 | Only authenticated assigned client may approve. |
| APP-02 | Round must be `open` and have at least one RoundPage. |
| APP-03 | All feedback must be `resolved`; `open` and `reopened` block approval. |
| APP-04 | Approval may proceed when there is no feedback (proposed policy). |
| APP-05 | Exactly one Approval record per round, enforced by OneToOne/unique constraint. |
| APP-06 | Approval actor/time come from authenticated session and server, not request payload. |
| APP-07 | Approval record creation and round status update occur atomically. |
| APP-08 | Concurrent approval and feedback changes are serialized/rechecked under transaction. |
| APP-09 | Approved records cannot be silently revoked or overwritten. |
| APP-10 | Approval is workflow confirmation, not a legally certified digital signature. |

## 7. Status transitions
```text
RevisionRound: draft -> open -> approved
Feedback:      open -> resolved -> reopened -> resolved -> ...
```
No transition out of `approved`. Feedback transitions are disabled after approval.

## 8. Acceptance scenarios (Given / When / Then)
### Authentication and access
**AC-01:** Given a logged-out visitor, when they request a protected project endpoint, then the API rejects access and returns no project data.

**AC-02:** Given client A and a project assigned to client B, when A requests that project, round, feedback or approval by direct ID, then the server rejects the request without exposing data.

**AC-03:** Given a client session, when the client attempts to create a project or publish a round, then the operation is denied and the database is unchanged.

### Projects and rounds
**AC-04:** Given staff and a valid client account, when staff creates a project with valid details, then it appears in staff and assigned-client views.

**AC-05:** Given an existing page slug in a project, when staff tries to create another page with the same slug, then validation rejects it.

**AC-06:** Given a draft round without pages, when staff publishes, then publishing fails with a clear error.

**AC-07:** Given an open round, when staff attempts to open a second round for the same project, then the server rejects it even under concurrent requests.

**AC-08:** Given a published round, when staff changes the project's page name, then the round's frozen page name remains unchanged.

**AC-09:** Given a round page, when staff attempts to attach a page from another project, then validation rejects the association.

### Feedback
**AC-10:** Given an assigned client viewing an open round, when they submit valid feedback, then an `open` record and `created` event are stored.

**AC-11:** Given whitespace-only feedback, when client submits it, then validation rejects it.

**AC-12:** Given open feedback, when staff resolves it with a note, then status becomes `resolved` and a history event records actor, note and timestamp.

**AC-13:** Given resolved feedback, when assigned client reopens with a reason, then status becomes `reopened` and the event history grows.

**AC-14:** Given open feedback, when client tries to resolve it, then access is denied and no event is created.

**AC-15:** Given an approved round, when any user attempts to add or modify feedback, then operation is rejected.

### Approval
**AC-16:** Given unresolved feedback, when assigned client tries to approve, then approval fails and no Approval record exists.

**AC-17:** Given all feedback resolved and a valid open round, when assigned client approves, then one Approval record is created and round becomes `approved` atomically.

**AC-18:** Given a round with no feedback, when assigned client approves, then approval succeeds under the proposed no-feedback policy.

**AC-19:** Given an already approved round, when approval is requested again, then no duplicate approval is created and a clear conflict/validation response is returned.

**AC-20:** Given two simultaneous approval requests, when both execute, then at most one Approval record exists and state remains consistent.

**AC-21:** Given approval of round 1, when round 2 is created, then round 1's approval actor, time, page snapshots and history remain unchanged.

### UX and operations
**AC-22:** Given API validation errors, when a form submission fails, then the UI shows actionable field or workflow errors and preserves safe user input.

**AC-23:** Given a narrow viewport and keyboard-only user, when navigating core screens, then controls remain usable with visible focus and meaningful labels.

**AC-24:** Given staging deployment, when the end-to-end project → revision → feedback → resolve/reopen → approve workflow runs, then all state changes persist correctly.

**AC-25:** Given a database backup, when a restore is rehearsed in an isolated environment, then core records and relationships can be recovered.

## 9. API conventions and validation
- Use standard HTTP semantics: `400` invalid input, `401` unauthenticated where API policy uses it, `403` forbidden, `404` unavailable/not found, `409` state conflict; exact response shape documented and tested.
- Avoid exposing project existence across client boundaries; choose a consistent 403/404 policy.
- CSRF tokens required for same-origin session-authenticated unsafe methods.
- Reject forged `approved_by`, timestamps, project ownership and role fields.
- Apply database constraints in addition to serializer validation.
- Use transactions and row locks for approval/publishing on MySQL; SQLite is not a substitute for production concurrency tests.

## 10. Test and completion standard
Each rule must have at least one automated positive or negative test, with priority on access isolation, state transitions, history immutability and concurrency. A feature is done only when UI/API behavior, validation, authorization, tests, documentation and code review are complete.

## 11. Decisions requiring confirmation
- Reviewer reassignment policy.
- Selected pages vs all pages in each revision.
- Whether approval with zero feedback is allowed.
- Whether an approved round can ever be revoked.
- Account provisioning/invitation approach.
- Retention/deletion policy.
