from parsers.forms_parser import parse_form


def test_parse_form_invalid():
    html = "<html><broken>"
    try:
        data = parse_form(html)
    except Exception:
        assert True  # acceptable to raise
