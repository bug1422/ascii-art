from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_info():
    response = client.get("/")
    print(response)
    assert response.status_code == 200
