from parsers.invoice_parser import parse_invoice

def test_parse_invoice_basic():
    html = """
    <html>
      <body>
        Αριθμός: INV-1001
        Ημερομηνία: 12/01/2024
        Πελάτης:
        John Doe

        Καθαρή Αξία: €150.00
        ΦΠΑ 24%: €24.00
        ΣΥΝΟΛΟ: €174.00
      </body>
    </html>
    """

    data = parse_invoice(html)

    assert data["invoice number"] == "INV-1001"
    assert data["date"] == "12/01/2024"
    assert data["customer name"] == "John Doe"

    # Money fields returned EXACTLY as strings (your parser keeps formatting)
    assert data["net total"] == "€150.00"
    assert data["vat amount"] == "€24.00"
    assert data["total"] == "€174.00"
