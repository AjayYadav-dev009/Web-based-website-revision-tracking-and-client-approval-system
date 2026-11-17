# Website Revision Tracking & Client Approval System

A web application for agencies to manage website review rounds, collect page-specific client feedback, track requested changes, and record formal approvals with an auditable history.

> **Status: In development.** This repository is being built toward a production-ready v1.0. Features described below are the intended scope, not a claim that they are already implemented.

## Why this exists

Website feedback is often scattered across email, chat, and spreadsheets. It becomes difficult to know which page and revision a comment refers to, whether an issue was resolved, and exactly what a client approved. This application centralizes the review workflow and preserves its history.

## Planned v1.0 features

- **Accounts and access:** staff and client roles, login/logout, project-level authorization.
- **Projects and pages:** staff-managed projects, client assignment, and page records.
- **Revision rounds:** numbered review cycles with page-specific preview URLs.
- **Feedback:** client comments on a particular page in a particular round; open, resolved, and reopened states.
- **Approval:** a designated client reviewer can approve an eligible round only when no unresolved feedback remains.
- **Audit history:** records of feedback changes, decisions, and approvals.
- **Dashboards:** dedicated staff and client interfaces.

### Important boundaries

This is **not** a website builder, source-control service, website host, or automatic screenshot comparison tool. It stores external preview URLs and review records. A saved URL does **not** guarantee the linked website's content will remain unchanged.

## Planned technology stack

| Area | Technology |
| --- | --- |
| Backend | Python, Django |
| REST API | Django REST Framework |
| Frontend | Django templates, HTML, CSS, vanilla JavaScript |
| Authentication | Same-origin Django sessions and CSRF protection |
| Database | SQLite for initial local development; MySQL planned for deployment |
| Architecture | Modular monolith with separated responsibilities |

## Architecture overview

```text
Browser (Django templates + JavaScript)
               |
        HTTP / JSON
               |
       Django + DRF
               |
   +-----------+-----------+
   |           |           |
Accounts    Projects     Reviews
   |           |           |
   +------- Django ORM ----+
               |
            Database
```

The intended Django apps are:

- `accounts/`: users, roles, authentication and permissions.
- `projects/`: projects, client assignments and website pages.
- `reviews/`: revision rounds, page previews, feedback, approval and audit records.
- `dashboard/`: server-rendered staff and client pages.
- `config/`: Django project settings and URL configuration.
- `templates/`, `static/`, `media/`: HTML templates, frontend assets and uploads.

These directories are **target architecture**, not a verified listing of the current repository.

## Local development

The steps below describe the **intended setup** once the Django scaffold and dependency file are committed. They are not a guarantee that every command works against the repository's current state.

### Prerequisites

- Python version compatible with the pinned Django release
- Git
- A terminal (PowerShell examples below)

### Setup on Windows (PowerShell)

```powershell
git clone <YOUR-REPOSITORY-URL>
cd <YOUR-REPOSITORY-FOLDER>
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Once `.env.example` exists, copy it to `.env` and set the documented development values. **Never commit `.env` or production secrets.**

After database configuration is complete:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. If PowerShell blocks activation, configure the execution policy appropriately for your environment or invoke `.\.venv\Scripts\python.exe` directly. Do not run `makemigrations` blindly against an unreviewed schema.

## Intended workflow

1. Staff creates a project and registers its website pages.
2. Staff creates a revision round and supplies preview URLs for the pages under review.
3. The designated client reviewer opens the round and submits page-specific feedback.
4. Staff addresses and resolves feedback; the client can reopen unsatisfactory issues.
5. When no unresolved issues remain, the client approves the eligible round.
6. The application retains the round's review and approval history.

All authorization and approval rules must be enforced by the backend, not only by hidden UI controls.

## API approach

The application will expose same-origin JSON endpoints under `/api/` using Django REST Framework. Proposed resources include projects, revision rounds, and feedback, with dedicated actions for resolving, reopening, and approving. Endpoint details and permission contracts are defined in `production.md` and must be implemented and tested before being considered available.

## Quality and security expectations

- Tests for permissions, input validation, state transitions, and approval restrictions.
- CSRF protection, secure session handling, and server-side access checks.
- No credentials, secret keys, or personal data in Git commits or logs.
- Responsive, accessible interfaces with useful error and empty states.
- Environment-specific settings, deployment checks, backups, restore testing, and rollback procedures.
- A feature is complete only when its acceptance criteria and Definition of Done are met.

## Project documentation

| File | Purpose |
| --- | --- |
| [`production.md`](production.md) | Detailed product and technical specification |
| [`ROADMAP_TODO.md`](ROADMAP_TODO.md) | Implementation checklist from planning to deployment |
| `README.md` | Project introduction and developer onboarding |

If implementation changes an architectural or product decision, update the relevant documentation and record the rationale.

## Current progress

**Planning and architecture documentation are prepared.** Implementation progress must be verified against the repository and checked off in `ROADMAP_TODO.md`. No unverified features are marked complete here.

## Deployment

A production host and exact infrastructure configuration have not yet been finalized. The release plan includes environment configuration, production database setup, static/media handling, HTTPS, application server configuration, migrations, backups, monitoring, staging verification, and rollback. See `ROADMAP_TODO.md` for the deployment checklist.

**Do not deploy using Django's development server (`runserver`).**

## Contributing

Use focused branches and pull requests, keep migrations with model changes, add tests for behavioral changes, and update documentation when workflows or API contracts change. Do not commit `.venv/`, `.env`, database dumps, or uploaded user data.

## License

No license has been selected yet. Until one is added, do not assume the repository is open-source or that reuse is permitted.
