from parsers.pipeline import run_full_scan
from core.models import ExtractedItem

def test_pipeline_creates_items(db, settings, tmp_path, monkeypatch):
    # Create temporary dummy_data folder
    dummy = tmp_path / "dummy_data"
    (dummy / "forms").mkdir(parents=True)
    (dummy / "emails").mkdir(parents=True)
    (dummy / "invoices").mkdir(parents=True)

    # Simple test form file
    f = dummy / "forms" / "form1.html"
    f.write_text('<input name="full_name" value="Test User">')

    # Point Django settings to new dummy_data directory
    monkeypatch.setattr(settings, "BASE_DIR", tmp_path)

    created, errors = run_full_scan()

    assert created == 1
    assert errors == 0
    assert ExtractedItem.objects.count() == 1
