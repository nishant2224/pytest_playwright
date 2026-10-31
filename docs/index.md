# Python Quality Demo

Welcome to the Python Quality Demo documentation. This repository is an independently written Python test automation platform targeting [Restful Booker Platform](https://automationintesting.online/), the public practice web application created by Mark Winteringham and contributors.

## Purpose

The project demonstrates a production-grade yet small, understandable automation framework using:
- **Playwright (synchronous)** for resilient browser automation.
- **pytest & pytest-bdd** for executable Gherkin feature scenarios and API testing.
- **HTTPX** for direct HTTP contract tests and test data ownership management.
- **Strict architecture**: distinct facade, action, assertion, and page object layers.
- **Data isolation**: run-, worker-, and scenario-unique identifiers with owned-record tracking.

## Navigation Guide

| Guide | What you will learn |
| --- | --- |
| [Getting Started](getting-started.md) | Setting up uv, Python 3.12+, installing browsers, and running your first test. |
| [Project Map](project-map.md) | Understanding architectural layers, facades, fixture lifetimes, and the vertical slice path. |
| [Writing Tests](writing-tests.md) | Where steps, actions, assertions, and selectors belong when adding or modifying scenarios. |
| [Running & Results](running-and-results.md) | Test markers, serial vs parallel execution, Allure reporting, and artifact inspection. |
| [Troubleshooting](troubleshooting.md) | Resolving common issues, timeout debugging, and reading owned-record cleanup manifests. |
| [Target Notes](target-notes.md) | Observations from live target verification and documented backend behavior. |

## Quick Command

To run the five non-writing verification tests right away:

```powershell
uv run pytest -m "not writes_data"
```
