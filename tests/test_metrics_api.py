# tests/test_metrics_api.py
from django.urls import reverse
from core.models import ExtractedItem


def test_metrics_status_counts(client, db):
    ExtractedItem.objects.create(source_type="form", source_file="a.html", status="pending", data={})
    ExtractedItem.objects.create(source_type="email", source_file="b.eml", status="approved", data={})
    ExtractedItem.objects.create(source_type="invoice", source_file="c.html", status="error", data={})

    resp = client.get(reverse("metrics_status"))
    assert resp.status_code == 200

    data = resp.json()
    assert "pending" in data
    assert "approved" in data
    assert "error" in data
    assert data["pending"] >= 1
    assert data["approved"] >= 1
    assert data["error"] >= 1


def test_metrics_source_counts(client, db):
    ExtractedItem.objects.create(source_type="form", source_file="a.html", status="pending", data={})
    ExtractedItem.objects.create(source_type="email", source_file="b.eml", status="pending", data={})
    ExtractedItem.objects.create(source_type="invoice", source_file="c.html", status="pending", data={})

    resp = client.get(reverse("metrics_source"))
    assert resp.status_code == 200

    data = resp.json()
    assert data.get("form", 0) >= 1
    assert data.get("email", 0) >= 1
    assert data.get("invoice", 0) >= 1


def test_metrics_daily_counts(client, db):
    ExtractedItem.objects.create(source_type="form", source_file="a.html", status="pending", data={})
    resp = client.get(reverse("metrics_daily"))
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) <= 14
    # Each row has date + 4 statuses
    for row in data:
        assert "date" in row
        for key in ["pending", "approved", "rejected", "error"]:
            assert key in row
