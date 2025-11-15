from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_csv_upload_and_query():
    content = "date,value\n2024-01-01,10\n2024-01-02,12\n"
    files = {"file": ("test.csv", io.BytesIO(content.encode("utf-8")), "text/csv")}
    r = client.post("/datasets/upload", files=files)
    assert r.status_code == 200
    dataset_id = r.json()["dataset_id"]

    payload = {"dataset_id": dataset_id, "query": "show me growth over time", "chart_lib": "matplotlib"}
    r2 = client.post("/charts/query", json=payload)
    assert r2.status_code == 200
    chart_id = r2.json()["chart_id"]

    r3 = client.get(f"/charts/{chart_id}")
    assert r3.status_code == 200
    data = r3.json()
    assert data["chart_type"] == "png"
    assert data["payload_base64"] is not None
