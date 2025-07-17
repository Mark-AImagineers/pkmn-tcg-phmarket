# AGENTS.md

This file defines the coding standards, structure, and expectations for **developers, collaborators, and AI agents** working on the `pokemon_tcg_market_ph` project.
Everything here is intentional. Please read carefully before writing, modifying, or generating code.

---

## Coding Philosophy

We follow clear, long-term principles:

- **KISS** – Keep It Simple and Self-explanatory
- **DRY** – Don’t Repeat Yourself
- **Clarity over cleverness** – Prioritize readability over tricks
- **Explicit over implicit** – Avoid “magic” or hidden logic
- **Modular by feature** – Group logic by what it does, not by type
- **Documented** – Every function, class, or service must have a purpose and docstring

---

## Guidelines

- Write clean, consistent Python 3.11+ code
- Follow PEP8 (with flexibility where readability matters)
- Use **type hints** consistently
- Use **docstrings** for:
  - All public functions and classes
  - Modules with meaningful logic
- Avoid global state and unnecessary complexity
- Never assume — every important behavior should be tested or documented
- Keep functions small and purpose-driven
- Group related logic in services (not bloated utils)

---

## Folder Structure (Initial Plan)

This structure will evolve, but this is the intended baseline.
```
pokemon_tcg_market_ph/
├── cards/
│   ├── models/
│   ├── views/
│   ├── api/
│   ├── services/
│   └── templates/cards/
├── collection/
├── marketplace/
├── trust/
├── templates/
├── static/
├── tests/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py
│   ├── wsgi.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── local.py
│       ├── staging.py
│       └── production.py
├── docker/
│   ├── dev/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   ├── prod/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
├── heroku/
│   ├── Procfile
│   ├── runtime.txt
│   └── app.json
├── .env
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── CHANGELOG.md
├── requirements.txt
└── version.json
```
---

## Development Rules

### Environment Consistency

- Local development must simulate the production environment as closely as possible.
- Use **Docker** to containerize and isolate environments, but **never write Docker-specific logic into the application codebase**.
- Environment-specific configuration must be abstracted through:
  - `.env` files
  - `os.environ` lookups
  - Modular settings files: `local.py`, `staging.py`, `production.py`
- **Never hardcode**:
  - credentials
  - database names
  - ports
  - file paths
  - hostnames
- Switching between environments must only require changing the `DJANGO_SETTINGS_MODULE` — no structural code changes.

---

### Security First

- Validate **all** inputs via:
  - Django Forms
  - DRF Serializers
  - Pydantic models (if used)
- **Never trust user input.** Always sanitize, validate, and whitelist allowed values.
- Use Django’s built-in **password hashing** (PBKDF2 or Argon2 via `passlib` if needed).
- In production:
  - Enforce **HTTPS**
  - Enable **CSRF protection**
  - Restrict **CORS settings**
- Never expose:
  - Internal service logic
  - Detailed error tracebacks
  - Database structures or raw IDs

---

### General Development Practices

- Use the `services/` folder to isolate business logic.
- Keep `views/` and `api/` files lean — only orchestrate, never embed logic.
- Prefer **class-based views** where possible.
- All code should be **testable**. If it's not, refactor it.
- Functions should:
  - Be short
  - Do one thing
  - Have descriptive names
- Avoid:
  - Global state
  - Hidden side effects
  - Circular imports
- Place reusable constants in `core/` or `settings/`, **not** scattered in logic.

---

### Testing & Formatting

- Testing uses **pytest** + `pytest-django`.
- Test structure should mirror the main app (`tests/<feature>/`)
- Format all code with **Black**:

  ```bash
  black .
  ```
- Use PEP8 as a guideline but prioritize readability.
- Add docstrings for:
    - All public functions
    - Classes
    - Modules with logic

### Dependency Management
All dependencies must be listed in requirements.txt.

Use version pinning for production:

```text
Copy
Edit
fastapi==0.110.0
uvicorn==0.29.0`
```
### Documentation
In each PR update the `CHANGLOG.md` and `version.json` version if needed
Follow semantic versioning

### Service Metadata
Every service must include a version.json file at the project root.

Example structure:

```json
{
  "name": "cards",
  "version": "0.1.0",
  "environment": "local",
  "release_notes": "Initial setup and cards API"
}
```

- Make this file available via a lightweight /version endpoint.
- This helps with:
  - CI/CD tagging
  - Service monitoring
  - Cross-environment debugging