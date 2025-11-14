from parsers.email_parser import parse_email

def test_parse_email_basic():
    raw = """
    From: John Doe <john@example.com>
    Subject: New Client

    Name: John
    Email: john@example.com
    Phone: 5551234
    """

    data = parse_email(raw)

    assert data["name"] == "John"
    assert data["email"] == "john@example.com"
    assert data["phone"] == "5551234"
