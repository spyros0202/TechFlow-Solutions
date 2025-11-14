import pytest
from parsers.forms_parser import parse_form

def test_parse_form_basic():
    html = """
    <form>
        <input name="full_name" value="John Doe">
        <input name="email" value="john@example.com">
        <input name="phone" value="5551234">
    </form>
    """
    data = parse_form(html)

    assert data["full name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["phone"] == "5551234"
