
## Project Overview

**django-microsoft-sso** is a Django library that simplifies Microsoft 365 authentication for Django Admin (and non-admin pages). It uses the Microsoft Identity Platform (MSAL) OAuth 2.0 flow to authenticate users and auto-create/update Django user records from Microsoft Graph API data.

Key features:
- Auto-create users from Microsoft 365 accounts
- Three hook points: pre_validate, pre_create, pre_login
- Callable settings (per-request/per-site configuration via Django Sites Framework)
- Secure POST callback mode with cache-backed state storage
- SLO (Single Logout) support
- Compatible with Django 5.0–6.0, Python 3.11–3.14

## Architecture

The library has two core dataclasses in `main.py`:

- **`MicrosoftAuth`** — Handles the OAuth 2.0 flow: builds auth URIs, acquires tokens via MSAL, fetches user info from Microsoft Graph, manages session/cache state.
- **`UserHelper`** — Handles user lookup, creation, permission assignment, and data updates from Microsoft Graph response data.

The auth flow (`views.py`):
1. `start_login` → initiates MSAL auth code flow, saves state in session or cache
2. `callback` → receives auth code, acquires token, fetches user info, runs three hooks (pre_validate → pre_create → pre_login), creates/retrieves user, logs them in

Settings are defined in `conf.py` via a `MicrosoftSSOSettings` class with a per-property pattern, delegating to Django's `settings` module. Module-level `__getattr__` (PEP 562) provides transparent access.

## Key Patterns

- **Hook system**: Three callbacks (`pre_validate_user`, `pre_create_user`, `pre_login_user`) defined in `hooks.py` with defaults. Configured via dotted-path strings in settings (e.g. `MICROSOFT_SSO_PRE_CREATE_CALLBACK`).
- **Callable settings**: Most settings accept either a plain value or a callable `(HttpRequest) -> value` for per-request/per-site configuration.
- **Settings as properties**: Every setting is a `@property` on `MicrosoftSSOSettings` using `_get_setting(name, default, accept_callable)`. Non-callable settings use `accept_callable=False`.
- **Dual callback modes**: `GET` (query, session-based state) or `POST` (form_post, cache-based state), controlled by `MICROSOFT_SSO_REQUIRE_SECURE_CALLBACK`.

## Commands

```bash
make install        # Install deps + pre-commit hooks
make lint           # Run pre-commit (black, flake8, isort)
make tests          # Run full pytest suite
make test <path>    # Run a single test, e.g.: make test megalus/tests/test_base_views.py::test_health_check
make update         # Update dependencies and pre-commit hooks
```

## Testing Conventions

- To run tests, use `make tests` to run all tests or `make test <test_path>` to run a single test.
- If you need to run using pytest command directly, set `STELA_ENV=test`
- Tests are always syncronous (no `async` tests) and should avoid external API calls (mock them instead). Use `pytest-mock` for mocking.
- When resolving tests, always resolve warnings too.

## Lint and Formatting

- Check lint using command `make lint`.
- The command `make lint` runs `pre-commit run --all` under the hood.
- This means when `ruff` and `bandit` runs, they will try to fix the issues automatically.
- When checking for lint, if the first `make lint` returns errors, run the command again before making any manual changes.


## Code Style

- Python 3.13, Django 6.0, Ruff for deps.
- Always use type hints. Use `TypedDict` for dicts with 5+ keys. Use `Enum`/`Literal` for fixed values. Use `X | None` not `Optional[X]`.
- Google-style docstrings for functions/classes >7 lines.
- f-strings, double quotes, triple quotes for multi-line.
- Prefer dataclasses over regular classes.
- Always use English in code, comments, tests, commits, and docs. If non-English content is needed, put it in a separate file and use `gettext` for translation.

## Commit Messages

One-line, semantic prefix based on changed files:
- `feat:` — changes in `django-microsoft-sso/` and `docs/`
- `refactor:` — changes in `django-microsoft-sso/` without test changes
- `ci:` — changes only in `.github/`, or `pyproject.toml`
- `chore:` — changes outside `django-microsoft-sso/` and `example_microsoft_app/`
- `docs:` — changes only in `docs/` or `README.md`
