from django.urls import reverse
from core.models import ExtractedItem

def test_export_excel_works(client, db):
    ExtractedItem.objects.create(
        source_type="email",
        source_file="email1.eml",
        data={"email": "x@example.com"},
        status="pending"
    )

    response = client.get(reverse("export_items") + "?status=all")

    assert response.status_code == 200
    assert response["Content-Type"].startswith(
        "application/vnd.openxmlformats-officedocument"
    )
    assert response["Content-Disposition"].endswith(".xlsx")
