import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_customers():
    response = client.get("/customers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
