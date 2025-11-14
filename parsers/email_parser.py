import re
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # Load GOOGLE_API_KEY and GEMINI_MODEL from .env

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

def safe_search(pattern, text):
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return None


def classify_email_with_gemini(email_text: str) -> str:
    """
    Use Gemini to classify the email type.
    Falls back to 'Unknown' if anything goes wrong.
    """

    # If no API key exists → skip classification
    if not GOOGLE_API_KEY:
        return "Unknown"

    prompt = f"""
    You are an email classifier. Categorize the email into EXACTLY one of the following types:

    - Client Inquiry
    - Invoice Notification
    
    Return ONLY the category name. No explanation.

    Email content:
    \"\"\"{email_text}\"\"\"
    """

    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        category = response.text.strip()
        return category
    except Exception:
        return "Unknown"

def parse_email(raw):
    data = {}

    # Classify the email first
    email_category = classify_email_with_gemini(raw)
    if email_category and email_category != "Unknown":
        data["category"] = email_category

    # Try structured parsing first (with labels) - supports both English and Greek
    name = safe_search(r"(?:Name|Όνομα):\s*(.*)", raw)
    email = safe_search(r"(?:Email):\s*(.*)", raw)
    phone = safe_search(r"(?:Phone|Κινητό|Τηλέφωνο):\s*(.*)", raw)

    # Also try to extract from bulleted lists
    if not name:
        name = safe_search(r"[-•]\s*(?:Όνομα|Name):\s*(.*)", raw)
    if not email:
        email = safe_search(r"[-•]\s*(?:Email):\s*(.*)", raw)
    if not phone:
        phone = safe_search(r"[-•]\s*(?:Κινητό|Phone|Τηλέφωνο):\s*(.*)", raw)

    if name:
        data["name"] = name
    if email:
        data["email"] = email
    if phone:
        data["phone"] = phone

    # If no structured data found, try to extract email addresses directly
    if not email:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_matches = re.findall(email_pattern, raw)
        if email_matches:
            # Filter out generic emails
            personal_emails = [e for e in email_matches if not e.startswith(('info@', 'contact@', 'support@'))]
            if personal_emails:
                data["email"] = personal_emails[0]
            elif email_matches:
                data["email"] = email_matches[0]

    # Extract phone numbers if not found with label
    if not phone:
        # Greek phone patterns (mobile: 69XX-XXXXXX, landline: 2XXX-XXXXXX)
        phone_pattern = r'(?:\+30\s?)?(?:69\d{2}[-\s]?\d{3}[-\s]?\d{3}|2[1-8]\d{2}[-\s]?\d{3}[-\s]?\d{3})'
        phone_match = re.search(phone_pattern, raw)
        if phone_match:
            data["phone"] = phone_match.group(0).strip()

    return data