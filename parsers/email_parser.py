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

    # Name
    m = re.search(r"Name:\s*(.*)", raw, re.IGNORECASE)
    if m:
        data["name"] = m.group(1).strip()

    # Email
    m = re.search(r"Email:\s*(.*)", raw, re.IGNORECASE)
    if m:
        data["email"] = m.group(1).strip()

    # Phone
    m = re.search(r"Phone:\s*(.*)", raw, re.IGNORECASE)
    if m:
        data["phone"] = m.group(1).strip()

    return data
