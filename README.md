# **TechFlow Automation Platform**
### *AthenaGen AI – Solutions Engineer Assignment*
**Author:** Spyros Vythoulkas

---

# **1. Overview**

This project implements a complete automation workflow for processing customer forms, emails, and invoices for the fictional company **TechFlow Solutions**.

The system provides:

- Automated data extraction from **HTML forms**, **emails (.eml)**, and **HTML/PDF-like invoices**
- A full **human-in-the-loop** validation and review process
- **Excel export** with automatic updates + multi-sheet support
- A modern **TailwindCSS dashboard** for reviewing/approving data
- Strong **error handling**, **logging**, and **test coverage**
- **Docker support** for reproducible deployment

The entire solution is powered by Django, TailwindCSS, BeautifulSoup4, Pandas, and Pytest.

---

# **2. Features**

## ✅ **Data Extraction Engine**
- Extracts structured fields from:
  - Website contact forms (HTML inputs)
  - Client emails (name, email, phone, messages)
  - Invoices (invoice number, totals, VAT, customer, notes)
- Handles malformed files gracefully using try/except boundaries
- Ensures missing fields are added as empty strings instead of crashing

## ✅ **Human-in-the-Loop Validation**
- Each extracted item becomes **pending**
- User can:
  - Review raw content
  - Edit extracted data manually
  - Approve / Reject / Save as pending
- No data ever enters Excel unless manually approved

## ✅ **Central Dashboard**
Features include:
- Status filters: Pending / Approved / Rejected / Error / All
- For each entry: ID, type, source file, summary, review button
- Live counters and Tailwind UI styling
- Graceful handling of empty states

## ✅ **Excel Integration**
- Auto-update Excel on approval
- Multi-sheet support based on `source_type`
- Fields auto-flattened into tabular structure
- Stored in `/exports/dashboard_export.xlsx`

## ✅ **Error Handling & Logging**
- Structured try/except handling across the entire pipeline
- Parser-level error capturing
- Excel export error recovery
- Django logging system enabled for:
  - pipeline errors
  - import failures
  - missing fields
- Items never crash the system; they become `"error"`

## ✅ **Test Suite**
Includes:
- Unit tests (forms, emails, invoices)
- Pipeline tests
- Dashboard + detail view tests
- Export engine tests
- End-to-end test using `dummy_data`
- 9 tests total

Run all tests:

```
pytest
```

---

# **3. System Architecture**

```
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
│   ├── templates/
│   │   ├── dashboard.html
│   │   ├── detail.html
│   │   └── base.html
│   └── views.py
│
├── dummy_data/
│   ├── forms/
│   ├── emails/
│   ├── invoices/
│   └── templates/
|
├── tests/
│   ├── test_forms_parser.py
│   ├── test_email_parser.py
│   ├── test_invoice_parser.py
│   ├── test_pipeline.py
│   ├── test_e2e_dummy_data.py
│   ├── test_export.py
│   ├── test_error_handling.py
│   ├── test_views_dashboard.py
│
└── manage.py
```

---

# **4. Docker Deployment**

Mandatory to have a .env file even if it's empty( with GOOGLE_API_KEY, optional)
## **Clone the repository**

```
git clone https://github.com/spyros0202/TechFlow-Solutions.git
cd TechFlow-Solutions
```
```
docker compose up --build
```
The app will be available at:  
👉 http://127.0.0.1:8001

---


# **6. Usage Guide**

### Run Full Scan  
Loads all files from `dummy_data/` and imports anything new.

### Review Items  
Go to dashboard → click **Review** to edit/view/approve.

### Approve Items  
On approval → item is exported to Excel automatically.

### Export Full Dashboard  
Download-the-dashboard button exports everything to XLSX.

---


# **7. License**

Internal Assignment – AthenaGen AI  
For evaluation purposes only.
