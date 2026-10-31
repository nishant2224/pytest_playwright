# Getting Started

This guide explains how to install prerequisites, set up the Python environment, and run the test suite.

## Prerequisites

- **Python 3.12+**: Installed and available on your PATH.
- **uv**: Modern, fast Python package and environment manager ([installation instructions](https://docs.astral.sh/uv/getting-started/installation/)).

## Setup Steps

### 1. Sync Dependencies

Run `uv sync` from the repository root. This resolves and installs all direct and development dependencies into a local `.venv/`:

```powershell
uv sync --frozen
```

*(On Linux / macOS: `uv sync --frozen`)*

### 2. Install Playwright Chromium

Download the matching Chromium browser binary used for UI scenarios:

```powershell
uv run playwright install chromium
```

### 3. Environment Configuration (Optional)

Copy the sample environment file if you wish to override credentials:

```powershell
Copy-Item .env.example .env
```

*(On Linux / macOS: `cp .env.example .env`)*

By default, the platform uses the publicly documented credentials (`admin` / `password`). No credentials or tokens are ever committed to Git.

### 4. Verify Test Collection

Verify that exactly six tests are discovered:

```powershell
uv run pytest --collect-only -q
```

Expected output:
```text
tests/api/test_enquiry_validation.py::test_missing_enquiry_subject_rejected
tests/api/test_rooms.py::test_public_room_list_contract
tests/bdd/test_admin_login.py::test_admin_login_success
tests/bdd/test_admin_login.py::test_admin_login_rejected
tests/bdd/test_guest_enquiry.py::test_guest_empty_enquiry_feedback
tests/bdd/test_guest_enquiry.py::test_guest_enquiry_reaches_admin_inbox
6 tests collected
```

### 5. Run API Tests (No Browser Required)

```powershell
uv run pytest -m api
```
