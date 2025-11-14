# AGAI Assignment - Solutions Engineer

---

1. Overview

This project implements a complete automation workflow for processing customer forms, emails, and invoices for the fictional company **TechFlow Solutions**.  
It integrates data extraction, human‑in‑the‑loop validation, Excel export, error handling, and a full dashboard UI.

The system is built with **Django**, **TailwindCSS**, and includes **Docker support**, **unit tests**, and a clean modular architecture.

---

2. Features

✅ Data Extraction
- HTML Forms → Structured customer data  
- Emails (EML) → Customer inquiries & contact details  
- Invoices (HTML/PDF-like) → Invoice numbers, totals, VAT, dates  

✅ Human‑in‑the‑Loop Workflow
- Dashboard for monitoring all items  
- Manual review screen  
- Approve / Reject / Save  
- Editable extracted fields  

✅ Excel Export
- Auto‑update master spreadsheet on approval  
- Multi‑sheet organization  
- Preserves formatting  
- Removes duplicates  
- Graceful handling of missing/invalid data  

✅ Robust Error Handling & Logging
- Try/except wrappers around all extraction pipelines  
- Logging per item (error_message field)  
- Red status for failed extractions  

✅ Testing
- Unit tests (forms, emails, invoices parsing)  
- Integration tests (pipeline, Excel export)  
- Full end‑to‑end dummy data test  

🐳 Docker Ready
- Dockerfile  
- docker‑compose.yml  
- Production & development modes  

---

3. System Architecture

Components
- **core/** → Models, utilities, Excel writer  
- **parsers/** → 3 independent parsers (forms, emails, invoices)  
- **dashboard/** → Views + templates  
- **tests/** → pytest + django integration tests  
- **dummy_data/** → Provided dataset  

Flow
1. User presses **Run Scan**  
2. System reads dummy_data/  
3. Each file is passed to its parser  
4. ExtractedItem is created with status:  
   - pending  
   - approved  
   - rejected  
   - error  
5. User reviews data  
6. Approved items are exported to Excel  

---

4. Installation

**Option A — Using Docker (recommended)**

```bash
docker compose build
docker compose up
```

App runs at:  
**http://localhost:8000**

**Option B — Local Python environment**

```bash
conda create -n agai_assignment python=3.10
conda activate agai_assignment
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

5. Usage Guide

Step 1 — Run the Scan
Click **Rescan Data** (top navigation bar).

Step 2 — Review Items
Dashboard displays:
- ID  
- Type  
- Source File  
- Status  

Click **Review** for details.

Step 3 — Edit Data
You can edit any extracted field before approval.

Step 4 — Approve or Reject
- Approve → Appends to Excel export file  
- Reject → Mark item as rejected  
- Save → Keep pending with modified data  

Step 5 — Export Dashboard
Go to:
```
/export?status=all
```
Download a full Excel report.

---

6. Folder Structure

```
automation_project/
│
├── core/
│   ├── models.py
│   ├── utils/
│   │   ├── excel.py
│   │   └── export_dashboard.py
│
├── parsers/
│   ├── forms_parser.py
│   ├── email_parser.py
│   ├── invoice_parser.py
│   ├── pipeline.py
│
├── dashboard/
│   ├── views.py
│   ├── templates/
│
├── tests/
├── dummy_data/
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

7. Testing

Run test suite:

```bash
pytest
```

Covers:
- Parsers  
- Dashboard views  
- Excel export  
- Dummy data E2E  

All tests **pass (9/9)**.

---

8. Technology Stack

- Django 5.2  
- Python 3.10  
- TailwindCSS  
- BeautifulSoup4  
- Pandas  
- Pytest  
- Docker + Compose  

---

9. Known Limitations

- Invoice parsing uses HTML structure (no PDF OCR)  
- Email parser supports basic EML format  

---

10. Future Extensions

- AI‑powered extraction (GPT‑4o)  
- Google Sheets live sync  
- Slack/Teams notifications  
- Analytics dashboard  
- Multi‑user authentication  

---

11. License
This project is provided exclusively for the AthenaGen AI Solutions Engineer assignment.

---

12. Contact
For questions:  
**spyrosvythoulkas@gmail.com**  

