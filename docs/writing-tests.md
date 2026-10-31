# Writing Tests

This guide explains how to extend or modify the test suite while preserving architectural boundaries and maintaining test independence.

## Boundary Rules

When adding new tests or modifying existing ones, place logic in the correct layer:

1. **Features (`.feature`)**:
   - Write clear, declarative Gherkin.
   - Never write selectors, CSS, XPath, or raw URLs in feature files.

2. **Step Definitions (`steps/`)**:
   - Keep steps thin.
   - Do not construct page objects or instantiate Playwright contexts inside steps.
   - Call facade `.actions` or facade `.assertions`.

3. **Actions (`actions.py`)**:
   - Model user workflows (e.g. `submit_enquiry`, `login`).
   - Coordinate page method calls.
   - Never duplicate selectors or assertions here.

4. **Assertions (`assertions.py`)**:
   - Always use Playwright's retrying matchers: `expect(locator).to_be_visible()`, `expect(page).to_have_url(...)`.
   - Never use `time.sleep()`.
   - Provide clear failure messages.

5. **Pages (`pages.py`) & Components (`components/`)**:
   - Own all locators.
   - Prefer stable test IDs (e.g. `[data-testid="ContactName"]`), standard HTML roles (`get_by_role("button", name="Submit")`), or scoped CSS (`#username`, `#password`).

## Worked Example: Adding an Assertion

Suppose you want to verify that the contact form's phone field requires a specific character length.

1. **Feature**:
   ```gherkin
   Then I see required-field feedback for phone
   ```

2. **Step Definition** (`enquiry_steps.py`):
   ```python
   @then("I see required-field feedback for phone")
   def assert_phone_feedback(guest_app: GuestApp) -> None:
       guest_app.assertions.phone_feedback_visible()
   ```

3. **Assertion** (`GuestAssertions`):
   ```python
   def phone_feedback_visible(self) -> None:
       expect(self.page.feedback_items.filter(has_text="Phone must be between")).to_be_visible()
   ```

4. **Page** (`ContactPage`):
   The locator `feedback_items` is already defined in `ContactPage`:
   ```python
   @property
   def feedback_items(self) -> Locator:
       return self.page.locator(".alert-danger p, .alert p")
   ```

## Test Independence

- Every test runs independently and provisions its own browser session or HTTP client.
- No test depends on the outcome or order of another test.
- The default collected test suite consists of exactly six focused cases (four BDD scenarios and two API tests).
