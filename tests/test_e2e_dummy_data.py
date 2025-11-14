from parsers.pipeline import run_full_scan

def test_e2e_full_dummy_data(client, db):
    created, errors = run_full_scan()

    assert created > 0
    assert errors >= 0

    # Export Excel
    response = client.get("/export/?status=all")

    assert response.status_code == 200
    assert b"PK" in response.content[:2]  # XLSX signature
