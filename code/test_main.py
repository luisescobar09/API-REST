from fastapi.testclient import TestClient
from main import app

clientes = TestClient(app)

def test_index():
    response = clientes.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "WENAS MAESTRO"}