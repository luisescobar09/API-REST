from fastapi.testclient import TestClient
from code.main_auth import app
import json
import requests
from requests.auth import HTTPBasicAuth

#python3 -m pytest -v
clientes = TestClient(app)

def test_index():
    response = clientes.get('/')
    data = {'mensaje' : 'API REST'}
    assert response.status_code == 200
    assert response.json() == data

def test_get_clientes_auth():
    auth = HTTPBasicAuth(username="user", password="user1")
    response = clientes.get('/clientes/', auth=auth)
    assert response.status_code == 401
    assert response.json() == {'detail' : 'Usuario o contraseña incorrecta'}

def test_get_clientes():
    auth = HTTPBasicAuth(username="user", password="user")
    response = clientes.get('/clientes/', auth=auth)
    data = [
        {
            "id_cliente": 1,
            "nombre": "Evelyn Jimenez",
            "email": "evelyn@gmail.com"
        },
        {
            "id_cliente": 2,
            "nombre": "Marco Polo Cruz",
            "email": "marco@gmail.com"
        },
        {
            "id_cliente": 3,
            "nombre": "José Luis Escobar",
            "email": "luis@gmail.com"
        }
    ]
    assert response.status_code == 202
    assert response.json() == data

def test_get_clientes_id_auth():
    auth = HTTPBasicAuth(username="admin", password="Admin")
    response = clientes.get('/clientes/2', auth = auth)
    assert response.status_code == 401
    assert response.json() == {'detail' : 'Usuario o contraseña incorrecta'}

def test_get_clientes_id():
    auth = HTTPBasicAuth(username="user", password="user")
    response = clientes.get('/clientes/2', auth = auth)
    data = {
            "id_cliente": 2,
            "nombre": "Marco Polo Cruz",
            "email": "marco@gmail.com"
        }
    assert response.status_code == 202
    assert response.json() == data  

def test_get_clientes_offset_limit_auth():
    auth = HTTPBasicAuth(username="admin", password="aadmin")
    response = clientes.get('/clientes/?offset=2&limit=010', auth = auth)
    assert response.status_code == 401
    assert response.json() == {'detail' : 'Usuario o contraseña incorrecta'}

def test_get_clientes_offset_limit():
    auth = HTTPBasicAuth(username="admin", password="admin")
    response = clientes.get('/clientes/?offset=2&limit=010', auth = auth)
    data = [
        {
            "id_cliente": 3,
            "nombre": "José Luis Escobar",
            "email": "luis@gmail.com"
        }
    ]
    assert response.status_code == 202
    assert response.json() == data

def test_post_cliente_auth():
    auth = HTTPBasicAuth(username="user", password="user")
    datos = {
        "nombre": "Cliente 1",
        "email": "cliente1@email.com"
    }
    response = clientes.post('/clientes/', data = json.dumps(datos), auth = auth)
    assert response.status_code == 403
    assert response.json() == {
        "detail": "No tienes permiso para acceder a este recurso."
    }

def test_post_cliente():
    auth = HTTPBasicAuth(username="admin", password="admin")
    datos = {
        "nombre": "Cliente 1",
        "email": "cliente1@email.com"
    }
    response = clientes.post('/clientes/', data = json.dumps(datos), auth = auth)
    assert response.status_code == 202
    assert response.json() == {
        "mensaje": "Cliente agregado"
    }

def test_put_cliente_auth():
    auth = HTTPBasicAuth(username="user", password="user")
    datos = {
        "id_cliente":4, 
        "nombre":"Cliente actualizado", 
        "email":"actualizado@email.com"
    }
    response = clientes.put('/clientes/', data = json.dumps(datos), auth = auth)
    assert response.status_code == 403
    assert response.json() == {
        "detail": "No tienes permiso para acceder a este recurso."
    }

def test_put_cliente():
    auth = HTTPBasicAuth(username="admin", password="admin")
    datos = {
        "id_cliente":4, 
        "nombre":"Cliente actualizado", 
        "email":"actualizado@email.com"
    }
    response = clientes.put('/clientes/', data = json.dumps(datos), auth = auth)
    assert response.status_code == 202
    assert response.json() == {
        "mensaje": "Cliente actualizado"
    }

def test_delete_cliente_auth():
    auth = HTTPBasicAuth(username="user", password="user")
    response = clientes.delete('/clientes/4', auth = auth)
    assert response.status_code == 403
    assert response.json() == {
        "detail": "No tienes permiso para acceder a este recurso."
    }

def test_delete_cliente():
    auth = HTTPBasicAuth(username="admin", password="admin")
    response = clientes.delete('/clientes/4', auth = auth)
    assert response.status_code == 202
    assert response.json() == {
        "mensaje": "Cliente borrado"
    }