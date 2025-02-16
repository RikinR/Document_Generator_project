from backend.app.routers.root import router
from fastapi.testclient import TestClient

client = TestClient(router)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "File Processing Service" in response.text