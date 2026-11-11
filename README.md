# Restful Booker API Test Automation

![API Tests](https://github.com/MufazaMajeed09/restful-booker-api-testing/actions/workflows/tests.yml/badge.svg)

Automated API tests for the [Restful Booker](https://restful-booker.herokuapp.com) hotel booking API, written in **Python** with **pytest** and **requests**, and run automatically with **GitHub Actions**.

## What is tested

| Area | Tests |
|---|---|
| Read | Get all bookings (200, non-empty list); get one booking (required fields and data types) |
| Create | Create a booking and check the saved data; retrieve it again (round-trip) |
| Authentication | Valid login returns a token; wrong password returns no token |
| Update | Update a booking with a token and confirm the change persisted |
| Delete | Delete with a token (201, then 404); delete **without** a token is refused (403) |
| Negative | Invalid booking IDs (`999999999`, `0`, `-1`, `abc`) return 404 |

## Key techniques
- **pytest fixtures** for the auth token and test bookings, with **automatic cleanup** (`yield` teardown), so no test data is left behind
- **Parametrized tests** for multiple invalid inputs
- **Schema checks** on response fields and types
- **Positive and negative testing**, including a security check (delete without a token)
- **CI/CD:** GitHub Actions runs every test on each push and pull request, and uploads an HTML report

## Project structure
```
restful-booker-api-testing/
├── .github/workflows/tests.yml   # CI pipeline
├── tests/
│   ├── conftest.py               # fixtures: auth_token, created_booking
│   └── test_bookings.py          # API tests
├── requirements.txt
└── README.md
```

## How to run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v --html=report.html --self-contained-html
```

## Test report
Each GitHub Actions run uploads an HTML report. Open **Actions**, choose a run, then download **api-test-report** under **Artifacts**.