TechFlow Automation Platform
AthenaGen AI – Solutions Engineer Assignment

Author: Spyros Vythoulkas

1. Overview

This project implements a complete automation workflow for processing customer forms, emails, and invoices for the fictional company TechFlow Solutions.

It includes:

Automated data extraction from forms, emails, and invoices

A full human-in-the-loop validation system

Excel export with automatic updates

Central dashboard for reviewing and approving items

Full error handling, logging, and test suite

Docker support for easy deployment

The solution is built with Django, TailwindCSS, BeautifulSoup4, Pandas, Pytest, and packaged with a robust modular architecture.

2. Features
✅ Data Extraction

HTML Forms → Extracts name, email, phone, company, service, message, etc.

Emails (EML format) → Extracts sender name, email, phone, subject, body content

Invoices (HTML/PDF-like) → Extracts invoice number, totals, VAT, dates

✅ Human-in-the-Loop Workflow

Dashboard showing all processed items

Manual edit view for each extracted item

Approve / Reject / Save options

Error status for failed extractions

Prevents duplicates & ensures full user control

✅ Excel Integration

Exports approved entries to a master spreadsheet

Auto-updates without overwriting old data

Graceful handling of formatting and missing fields

Can export filtered dashboard view (pending/approved/rejected/error/all)

✅ Error Handling & Logging

Try/except wrappers around all extraction logic

Errors stored in the database per item (error_message)

UI indicators for errors

Logging for pipeline operations

✅ Testing Suite

Unit tests for each parser

Integration tests for the pipeline

E2E test for full dummy_data ingestion

Dashboard rendering tests

Excel export tests

🐳 Docker Support

Dockerfile

docker-compose with auto-migrations

One-command startup

3. Architecture
High-Level Flow
dummy_data/ → pipeline → ExtractedItem(DB) → Dashboard → Review → Approve → Excel

Folder Structure
automation_project/
│
├── core/
│   ├── models.py
│   ├── utils/
│   │   ├── excel.py
│   │   ├── export_dashboard.py
│   │   └── logger.py
│
├── parsers/
│   ├── forms_parser.py
│   ├── email_parser.py
│   ├── invoice_parser.py
│   └── pipeline.py
│
├── dashboard/
│   ├── views.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   └── detail.html
│
├── tests/
│   ├── test_forms_parser.py
│   ├── test_email_parser.py
│   ├── test_invoice_parser.py
│   ├── test_pipeline.py
│   ├── test_export.py
│   ├── test_views_dashboard.py
│   └── test_e2e_dummy_data.py
│
├── dummy_data/
├── docker-compose.yml
├── Dockerfile
└── README.md

4. Installation
Option A — Run with Docker (Recommended)
docker compose build
docker compose up


Visit:

➡️ http://localhost:8000

All migrations + Tailwind + Django run automatically.

Option B — Run Locally
Create & activate environment:
conda create -n agai_assignment python=3.10
conda activate agai_assignment

Install dependencies:
pip install -r requirements.txt

Run setup:
python manage.py migrate
python manage.py runserver

5. Usage Guide
1. Run Full Scan

Press Rescan Data on the navigation bar.

This triggers:

Parsing all forms/emails/invoices

Deduplication (no double processing)

Error classification

Insertion into database

2. Review Items

The dashboard shows:

ID

Type

Source file

Status

Statuses:

Pending

Approved

Rejected

Error

3. Detail View

For each item you can:

Edit any field

Approve → exports to Excel

Reject → mark as rejected

Save → keep as pending

4. Export

Export all items or by status:

/export?status=all


Or use Dashboard button.

5. Excel Output

The system maintains:

Clean formatting

Unique rows

Auto-appending rows

Graceful handling of missing values

6. Testing

Run full test suite:

pytest


Tests included:

✔ Unit Tests

forms_parser

email_parser

invoice_parser

✔ Integration Tests

pipeline

Excel writer

dashboard views

✔ End-to-End Tests

Full dummy_data scan start → finish

All final tests:
8 passed, 0 failed

7. Technology Stack
Layer	Technology
Backend	Django 5.2
Parsing	BeautifulSoup4, re
Storage	SQLite
Frontend	TailwindCSS
Export	Pandas
Testing	Pytest + pytest-django
Deployment	Docker + docker-compose
8. Known Limitations

Invoice extraction is HTML-based (no PDF OCR)

Email extraction assumes structured EML format

Google Sheets sync is manual (Excel only built-in)

9. Future Enhancements

GPT-4o powered extraction (AI parsing)

Real-time Slack/Email alerts

Google Sheets live sync (Sheets API)

Multi-user authentication

Full analytics dashboard

10. License

This project is built exclusively for the AthenaGen AI Solutions Engineer Assignment.

11. Contact

📧 spyrosvythoulkas@gmail.com

For any questions or clarifications.
