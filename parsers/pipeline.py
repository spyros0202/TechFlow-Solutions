import logging
import pathlib
from django.conf import settings

from core.models import ExtractedItem
from parsers.forms_parser import parse_form
from parsers.email_parser import parse_email
from parsers.invoice_parser import parse_invoice

logger = logging.getLogger(__name__)


def run_full_scan():
    created = 0
    errors = 0

    base = pathlib.Path(settings.BASE_DIR) / "dummy_data"
    logger.info("Starting full scan in %s", base)

    # FORMS
    forms_dir = base / "forms"
    for file in forms_dir.glob("*.html"):
        if ExtractedItem.objects.filter(source_file=file.name).exists():
            logger.info("Skipping already imported form: %s", file.name)
            continue  # NO DUPLICATES

        raw = file.read_text(encoding="utf-8", errors="ignore")
        item = ExtractedItem(
            source_type="form",
            source_file=file.name,
            raw_content=raw,
        )
        try:
            item.data = parse_form(raw)
            item.status = "pending"
            item.save()
            created += 1
            logger.info("Imported form: %s", file.name)
        except Exception as e:
            item.status = "error"
            item.error_message = str(e)
            item.save()
            errors += 1
            logger.exception("Error parsing form %s", file.name)

    # EMAILS
    emails_dir = base / "emails"
    for file in emails_dir.glob("*.eml"):
        if ExtractedItem.objects.filter(source_file=file.name).exists():
            logger.info("Skipping already imported email: %s", file.name)
            continue

        raw = file.read_text(encoding="utf-8", errors="ignore")
        item = ExtractedItem(
            source_type="email",
            source_file=file.name,
            raw_content=raw,
        )
        try:
            item.data = parse_email(raw)
            item.status = "pending"
            item.save()
            created += 1
            logger.info("Imported email: %s", file.name)
        except Exception as e:
            item.status = "error"
            item.error_message = str(e)
            item.save()
            errors += 1
            logger.exception("Error parsing email %s", file.name)

    # INVOICES
    invoices_dir = base / "invoices"
    for file in invoices_dir.glob("*.html"):
        if ExtractedItem.objects.filter(source_file=file.name).exists():
            logger.info("Skipping already imported invoice: %s", file.name)
            continue

        raw = file.read_text(encoding="utf-8", errors="ignore")
        item = ExtractedItem(
            source_type="invoice",
            source_file=file.name,
            raw_content=raw,
        )
        try:
            item.data = parse_invoice(raw)
            item.status = "pending"
            item.save()
            created += 1
            logger.info("Imported invoice: %s", file.name)
        except Exception as e:
            item.status = "error"
            item.error_message = str(e)
            item.save()
            errors += 1
            logger.exception("Error parsing invoice %s", file.name)

    logger.info("Full scan completed: %s created, %s errors", created, errors)
    return created, errors
