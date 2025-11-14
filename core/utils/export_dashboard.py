from io import BytesIO
from pathlib import Path

import pandas as pd
from django.conf import settings

from core.models import ExtractedItem

EXPORT_PATH = Path(settings.BASE_DIR) / "dashboard_snapshot.xlsx"

# Hints for numeric columns
NUMERIC_HINTS = ["total", "amount", "vat", "net", "price"]


def _query_to_dataframe(qs):
    """
    Μετατρέπει ένα queryset από ExtractedItem σε DataFrame,
    flatten-άροντας το JSON field `data`.
    """
    rows = []

    for item in qs:
        base = {
            "id": item.id,
            "status": item.status,
            "source_type": item.source_type,
            "source_file": item.source_file,
        }
        data = item.data or {}
        for k, v in data.items():
            base[k] = v
        rows.append(base)

    if not rows:
        return pd.DataFrame(columns=["id", "status", "source_type", "source_file"])

    df = pd.DataFrame(rows)

    # Convert numeric-looking columns to numbers
    for col in df.columns:
        lower = col.lower()
        if any(hint in lower for hint in NUMERIC_HINTS):
            df[col] = pd.to_numeric(df[col], errors="ignore")

    return df


def build_multi_sheet_workbook(status_filter: str | None = None) -> BytesIO:
    """
    Δημιουργεί multi-sheet Excel με:
    - All
    - Forms
    - Emails
    - Invoices
    Προαιρετικά εφαρμόζει status filter.
    """
    if status_filter and status_filter != "all":
        base_qs = ExtractedItem.objects.filter(status=status_filter)
    else:
        base_qs = ExtractedItem.objects.all()

    all_df = _query_to_dataframe(base_qs)
    forms_df = _query_to_dataframe(base_qs.filter(source_type="form"))
    emails_df = _query_to_dataframe(base_qs.filter(source_type="email"))
    invoices_df = _query_to_dataframe(base_qs.filter(source_type="invoice"))

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        all_df.to_excel(writer, sheet_name="All", index=False)
        forms_df.to_excel(writer, sheet_name="Forms", index=False)
        emails_df.to_excel(writer, sheet_name="Emails", index=False)
        invoices_df.to_excel(writer, sheet_name="Invoices", index=False)

    output.seek(0)
    return output


def update_dashboard_snapshot():
    """
    Auto-update αρχείο dashboard_snapshot.xlsx με ΟΛΑ τα items.
    Καλείται μετά από approve/reject/save.
    """
    buffer = build_multi_sheet_workbook(status_filter="all")

    with open(EXPORT_PATH, "wb") as f:
        f.write(buffer.getbuffer())
