# Applicant Qualification Expert System (Python)

This project implements a rule-based expert system in Python (Flask) that evaluates applicants for:

- Entry-Level Python Engineer
- Python Engineer
- Project Manager
- Senior Knowledge Engineer

The app collects applicant information, validates strict input formats, and returns:

- Position(s) qualified for
- Position(s) not qualified for, with exact disqualifying reasons

## Source Code

- `/Users/jonnykateharron/Documents/New project/app.py`
- `/Users/jonnykateharron/Documents/New project/templates/index.html`
- `/Users/jonnykateharron/Documents/New project/static/styles.css`
- `/Users/jonnykateharron/Documents/New project/requirements.txt`

## Run In VS Code

1. Open folder in VS Code:
   - `code "/Users/jonnykateharron/Documents/New project"`
2. Create and activate a virtual environment:
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Start server:
   - `python3 app.py`
5. Open executable URL:
   - `http://127.0.0.1:5000`

## Validation Rules

- Degree must be exactly one of:
  - `Bachelor in CS`
  - `Masters in CS`
  - `Bachelor and Masters in CS`
  - `None`
- Certification must be exactly one of:
  - `PMI Lean Project Management Certification`
  - `None`
- Experience fields must be whole numbers from `0` to `100`.

Invalid input is rejected with clear correction messages (for example, entering `BS` is rejected).
