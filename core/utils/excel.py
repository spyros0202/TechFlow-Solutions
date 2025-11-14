import pandas as pd
from pathlib import Path
from django.conf import settings

TEMPLATE_CSV = Path(settings.BASE_DIR) / "dummy_data" / "templates" / "data_extraction_template.csv"
OUTPUT_XLSX = Path(settings.BASE_DIR) / "extracted_data.xlsx"


def ensure_excel_exists():
    """
    Creates extracted_data.xlsx from template CSV if not already present.
    """
    if not OUTPUT_XLSX.exists():
        df = pd.read_csv(TEMPLATE_CSV)
        df.to_excel(OUTPUT_XLSX, index=False)
        print("Excel file created from template.")


def append_item_to_excel(item):
    """
    Add an approved item to extracted_data.xlsx following template structure.
    Missing fields are left empty.
    """
    ensure_excel_exists()

    df = pd.read_excel(OUTPUT_XLSX)

    new_row = {}

    # follow template columns exactly
    for col in df.columns:

        # field exists in parsed data
        if item.data and col in item.data:
            new_row[col] = item.data[col]

        # metadata fields
        elif col == "source_type":
            new_row[col] = item.source_type
        elif col == "source_file":
            new_row[col] = item.source_file
        elif col == "status":
            new_row[col] = item.status

        # otherwise keep empty
        else:
            new_row[col] = ""

    df.loc[len(df)] = new_row
    df.to_excel(OUTPUT_XLSX, index=False)
