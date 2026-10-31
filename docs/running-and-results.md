# Running Tests & Understanding Results

This document describes how to execute tests using `pytest` or the `quality-demo` CLI, filter with markers, and inspect test evidence and Allure reports.

## Execution Commands

### Running with pytest

```powershell
# Run all tests (default serial execution)
uv run pytest

# Run only API contract tests (no browser launched)
uv run pytest -m api

# Run only BDD UI scenarios
uv run pytest -m bdd

# Run reduced suite excluding data-writing tests (while live DELETE returns 500)
uv run pytest -m "not writes_data"

# Run smoke tests
uv run pytest -m smoke
```

### Running with the quality-demo CLI

The `quality-demo` entry point provides an intuitive interface for running test profiles:

```powershell
# Dry run: view translated pytest arguments without execution
uv run quality-demo --target demo --markers e2e --dry-run

# Run API tests
uv run quality-demo --target demo --markers api

# Run headed in a visible browser
uv run quality-demo --target demo --markers smoke --headed
```

## Test Markers

Strict marker checking is enabled. Allowed markers are:
- `bdd`: BDD scenarios executed via pytest-bdd.
- `ui`: UI tests driving browser automation.
- `auth`: Authentication scenarios (valid and invalid logins).
- `smoke`: Core smoke check scenarios.
- `negative`: Negative input and validation failure checks.
- `e2e`: End-to-end integration workflows across guest and admin interfaces.
- `writes_data`: Tests that write data to the target and require ownership cleanup.
- `api`: Direct HTTP contract tests with no browser dependency.

## Test Artifacts and Evidence

When tests execute, outputs are stored in `artifacts/`:
- **Failure Screenshots**: Open guest and admin browser pages are captured upon failure and saved under `artifacts/evidence/<node_id>/`.
- **Owned-Records Manifest**: When record cleanup encounters an error (such as HTTP 500), an owned-record manifest is saved under `artifacts/owned-records/<run_id>/<worker_label>/<node_id>.json`.

## Allure Reporting

Allure output is opt-in. Generating raw results and rendering HTML reports are distinct steps:

### 1. Generate Raw Results

```powershell
$runId = Get-Date -Format 'yyyyMMdd-HHmmss'
uv run pytest -m bdd --alluredir "artifacts/allure/$runId"
```

*Note: The `allure-pytest-bdd` listener reports the four Gherkin BDD scenarios. Standard JUnit / terminal output covers all six tests.*

### 2. Render HTML Report (Optional Allure CLI)

If you have the standalone Allure CLI installed:

```powershell
allure generate "artifacts/allure/$runId" -o "artifacts/allure-report/$runId"
allure open "artifacts/allure-report/$runId"
```
