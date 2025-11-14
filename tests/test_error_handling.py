from parsers.forms_parser import parse_form


def test_parse_form_invalid():
    html = "<html><broken>"

    # Parser should NEVER throw — this is the key rule
    data = parse_form(html)

    # Must always return a dict
    assert isinstance(data, dict)

    # Required keys must exist
    expected_keys = [
        "full name",
        "email",
        "phone",
        "company",
        "service",
        "message",
        "priority",
        "submission date",
    ]

    for k in expected_keys:
        assert k in data

    # Values should be empty strings (or None)
    for v in data.values():
        assert v == "" or v is None
