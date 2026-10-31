# Troubleshooting Guide

This guide describes common symptoms, root causes, and recommended solutions.

## Common Issues

### 1. Missing Browser Binaries

**Symptom:**
```text
playwright._impl._errors.Error: Executable doesn't exist at ...
```

**Resolution:**
Install the Chromium browser binary for Playwright:
```powershell
uv run playwright install chromium
```

---

### 2. Live Target Deletion Returns HTTP 500

**Symptom:**
In `test_guest_enquiry_reaches_admin_inbox`, the test body passes (`PASSED`), but teardown errors:
```text
RuntimeError: Cleanup DELETE returned 500 for record <id>. Manifest written to artifacts/owned-records/...
```

**Root Cause:**
On the public hosted deployment of Restful Booker Platform, `DELETE /api/message/{id}` currently returns HTTP 500 (as documented in [Target Notes](target-notes.md)).

**Resolution:**
- This is a known hosted target blocker, not a framework bug. The framework honestly reports the error and preserves the owned-record manifest under `artifacts/owned-records/<run_id>/<worker_label>/`.
- To run a completely green validation suite excluding the data-writing scenario, use:
  ```powershell
  uv run pytest -m "not writes_data"
  ```

---

### 3. Connection Timeout or Hosted Target Outage

**Symptom:**
```text
playwright._impl._errors.TimeoutError: Page.goto: Timeout 30000ms exceeded.
```

**Resolution:**
- Verify your internet connectivity.
- Check whether `https://automationintesting.online/` is accessible in a normal browser.
- Adjust timeouts in `config/demo.toml` if network latency is unusually high.

---

### 4. Login Fails Unexpectedly

**Symptom:**
`test_admin_login_success` times out waiting for `/admin/rooms`.

**Resolution:**
- Confirm that the demo administrator credentials have not been changed on the hosted instance.
- Check `.env` to verify whether `RBP_ADMIN_USERNAME` or `RBP_ADMIN_PASSWORD` was set to an incorrect value.
