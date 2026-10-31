# Target Verification Notes

These notes summarize observations from live inspection of [Restful Booker Platform](https://automationintesting.online/) on 31 October 2026.

## Target Details

- **Hosted URL**: [https://automationintesting.online/](https://automationintesting.online/)
- **Admin URL**: [https://automationintesting.online/admin](https://automationintesting.online/admin)
- **Official Repository**: [Mark Winteringham / restful-booker-platform](https://github.com/mwinteringham/restful-booker-platform)
- **Maintainer API Documentation**: [Postman Collection](https://www.postman.com/automation-in-testing/restful-booker-collections/documentation/ci13ds3/restful-booker-platform)

## Verified Endpoints & UI Elements

| Feature / Route | Observed Behavior | Test Suite Implementation |
| --- | --- | --- |
| **Contact Form** | Five fields: `ContactName`, `ContactEmail`, `ContactPhone`, `ContactSubject`, `ContactDescription`. Submit button. | Covered by `test_guest_empty_enquiry_feedback` (T03) and `test_guest_enquiry_reaches_admin_inbox` (T04). |
| **Admin Login** | `#username`, `#password`, `#doLogin`. Valid login routes to `/admin/rooms`. Invalid credentials show `.alert.alert-danger`. | Covered by `test_admin_login_success` (T01) and `test_admin_login_rejected` (T02). |
| **Admin Inbox** | `/admin/message` displays message rows with sender name and subject. | Verified in T04 by exact subject and name matching. |
| **GET /api/room** | Anonymous `GET /api/room` returns 200 with JSON `{ "rooms": [...] }`. | Contract verified in `test_public_room_list_contract` (T05). |
| **POST /api/auth/login** | Returns 200 with `{ "token": "..." }`. Does not set cookie in response header. | Handled in `ApiClient.login()` by setting `token` cookie explicitly. |
| **POST /api/message** | Valid submission returns 200 with `{ "success": true }`. Submission without `subject` returns 400 with validation list. | Negative contract verified in `test_missing_enquiry_subject_rejected` (T06). |
| **GET /api/message/{id}** | Returns HTTP 500 on live deployment; details modal unavailable. | Full-detail dialog verification deferred until hosted endpoint recovers. |
| **DELETE /api/message/{id}** | Authenticated DELETE returns HTTP 500 for owned records. | Attempted in teardown; records manifest and produces visible teardown error. |

## Defect and Cleanup Findings

- Two fictional records were created during target verification and in test runs.
- The hosted backend returns HTTP 500 when attempting `DELETE /api/message/{id}` with a valid admin token.
- Because cleanup returns 500, the full test suite cannot honestly claim a completely green run without skipping or masking errors.
- The framework treats cleanup failures as errors (`ERROR` in pytest teardown) and saves an owned-record manifest under `artifacts/owned-records/`.
- Running `uv run pytest -m "not writes_data"` provides a clean 5-test suite for CI/review when non-writing verification is desired.
