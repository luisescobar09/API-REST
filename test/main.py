from fastapi.testclient import TestClient
from code.main import app
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

def test_get_clientes():
    response = clientes.get('/clientes/')
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
    assert response.status_code == 200
    assert response.json() == data

def test_get_clientes_id():
    response = clientes.get('/clientes/3')
    data = {
            "id_cliente": 3,
            "nombre": "Marco Polo Cruz",
            "email": "marco@gmail.com"
        }
    assert response.status_code == 200
    assert response.json() == data  

def test_get_clientes_offset_limit():
    response = clientes.get('/clientes/?offset=2&limit=010')
    data = [
        {
            "id_cliente": 3,
            "nombre": "José Luis Escobar",
            "email": "luis@gmail.com"
        }
    ]
    assert response.status_code == 200
    assert response.json() == data

def test_post_cliente():
    datos = {
        "nombre": "Cliente 1",
        "email": "cliente1@email.com"
    }
    response = clientes.post('/clientes/', data = json.dumps(datos))
    assert response.status_code == 200
    assert response.json() == {
        "mensaje": "Cliente agregado"
    }

def test_put_cliente():
    datos = {
        "id_cliente":4, 
        "nombre":"Cliente actualizado", 
        "email":"actualizado@email.com"
    }
    response = clientes.put('/clientes/', data = json.dumps(datos))
    assert response.status_code == 200
    assert response.json() == {
        "mensaje": "Cliente actualizado"
    }

def test_delete_cliente():
    response = clientes.delete('/clientes/4')
    assert response.status_code == 200
    assert response.json() == {
        "mensaje": "Cliente borrado"
    }

'''
def test_post_producto_4():
    auth = HTTPBasicAuth(username="user", password="user")
    payload = {"sku":"a","producto":"Nuevo","precio":30.0}
    response = productos.post(
        "/productos/",
        json=payload,
        auth=auth,
        headers={"content-type": "application/json"}
    )
    data = {"mensaje": "El item se agrego"}
    assert response.status_code == 202
    assert response.json() == data
'''