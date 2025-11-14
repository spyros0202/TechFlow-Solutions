from bs4 import BeautifulSoup

def parse_form(raw_html: str):
    soup = BeautifulSoup(raw_html, "html.parser")

    def get_input(name):
        tag = soup.find(["input", "textarea", "select"], attrs={"name": name})
        if tag is None:
            return ""
        if tag.name == "select":
            option = tag.find("option", selected=True)
            return option.get_text(strip=True) if option else ""
        return tag.get("value", "").strip() if tag.name == "input" else tag.get_text(strip=True)

    data = {
        "full name": get_input("full_name"),
        "email": get_input("email"),
        "phone": get_input("phone"),
        "company": get_input("company"),
        "service": get_input("service"),
        "message": get_input("message"),
        "priority": get_input("priority"),
        "submission date": get_input("submission_date"),
    }

    return data
