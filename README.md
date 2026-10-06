# Python Quality Platform

A starter repository for API tests with HTTPX and browser tests with Playwright.

## Directory layout

```text
python-quality_platform/
├── .gitignore
├── README.md
├── requirements.txt
├── pytest.ini
├── src/
│   └── __init__.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── api/
    │   └── .gitkeep
    └── ui/
        └── .gitkeep
```

Root files hold configuration and dependencies. Put reusable helpers in `src/`,
shared pytest fixtures in `tests/conftest.py`, API tests in `tests/api/`, and
browser tests in `tests/ui/`. The `.gitkeep` placeholders preserve empty test
directories in Git; remove them when adding tests.

## Setup on Windows (PowerShell)

Run from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

Activation makes `python` and `pip` use this project's isolated environment.
If PowerShell blocks activation, use the virtual environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install --with-deps chromium
.\.venv\Scripts\python.exe -m pytest
```

On macOS/Linux, create the environment with `python3 -m venv .venv` and activate
it with `source .venv/bin/activate`, then run the same installation commands.

## Dependencies

- `pytest`: test discovery, execution, fixtures, and assertions.
- `playwright`: browser automation.
- `pytest-playwright`: Playwright fixtures for pytest.
- `httpx`: HTTP client for API testing.

The versions in `requirements.txt` are minimum constraints (`>=`), not exact
pins. Later installations can resolve newer compatible releases.

## Run tests

```powershell
python -m pytest
python -m pytest -m smoke
python -m pytest -m api
python -m pytest -m ui
```

Name test files `test_*.py` and test functions `test_*`. Apply markers using
`@pytest.mark.smoke`, `@pytest.mark.api`, or `@pytest.mark.ui`; directory names
do not automatically apply markers. `pytest.ini` discovers tests under `tests/`
and enables verbose output with short tracebacks.

This scaffold contains no tests yet, so pytest reports "no tests ran" and
returns exit code 5 until tests are added.

## Git

The initial repository is created with:

```powershell
git init
git add .
git commit -m "chore: scaffold repository skeleton and dependencies"
```

The virtual environment, Python caches, and test artifacts are excluded by
`.gitignore`.
