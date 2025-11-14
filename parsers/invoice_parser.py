import re
from bs4 import BeautifulSoup

def clean_money(v):
    if not v:
        return ""
    # Keep the value EXACTLY as written (including € and commas)
    return v.strip()

def parse_invoice(raw_html: str):
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text("\n", strip=True)

    def find(pattern):
        m = re.search(pattern, text, re.MULTILINE | re.UNICODE)
        return m.group(1).strip() if m else ""

    data = {
        # Basic invoice info
        "invoice number": find(r"Αριθμός:\s*([A-Za-z0-9\-\/]+)"),
        "date": find(r"Ημερομηνία:\s*([0-9]{2}\/[0-9]{2}\/[0-9]{4})"),
        "customer name": find(r"Πελάτης:\s*\n(.*)"),

        # Summary amounts
        "net total": clean_money(find(r"Καθαρή Αξία:\s*(€[\d\.,]+)")),
        "vat amount": clean_money(find(r"ΦΠΑ\s*24%:\s*(€[\d\.,]+)")),
        "total": clean_money(find(r"ΣΥΝΟΛΟ:\s*(€[\d\.,]+)")),
    }

    # Optional text fields
    notes = find(r"Σημειώσεις:\s*(.*)")
    delivery = find(r"Παράδοση:\s*(.*)")

    if notes:
        data["notes"] = notes

    if delivery:
        data["delivery"] = delivery

    return data
