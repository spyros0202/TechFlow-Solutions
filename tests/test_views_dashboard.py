from django.urls import reverse
from core.models import ExtractedItem

def test_dashboard_loads(client, db):
    ExtractedItem.objects.create(
        source_type="form",
        source_file="a.html",
        data={"full_name": "Test"},
        status="pending"
    )

    resp = client.get(reverse("dashboard"))
    assert resp.status_code == 200

    # Dashboard shows source_file, not data fields
    assert b"a.html" in resp.content

def test_detail_approve(client, db):
    item = ExtractedItem.objects.create(
        source_type="form",
        source_file="a.html",
        data={"full_name": "Test"},
        status="pending",
    )

    url = reverse("detail", args=[item.id])

    resp = client.post(url, {"action": "approve"})
    item.refresh_from_db()

    assert item.status == "approved"
