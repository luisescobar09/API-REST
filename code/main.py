from fastapi import FastAPI

import sqlite3
from typing import List, Optional
from pydantic import BaseModel

class Respuesta(BaseModel): #Modelado de los datos
    mensaje: str
class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str
class Post(BaseModel): #Validar los datos de entrada de POST y PUT
    id_cliente: Optional[int]
    nombre: str
    email: str

app = FastAPI()
ruta = 'sql/clientes.sqlite'

@app.get("/", response_model = Respuesta) #Primer endpoint
async def index():
    return {"mensaje": "API REST"}

@app.get("/clientes/") #Segundo endpoint
async def get_clientes(offset: int = 0, limit: int = 10): #parametros de consulta de tipo entero
    with sqlite3.connect(ruta) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CLIENTES LIMIT ? OFFSET ?;",(limit, offset),)
        respuesta = cursor.fetchall() #Si es válido envía la consulta de ese registro
        return respuesta

@app.get("/clientes/{id_cliente}") #Ahora como el segundo endpoint pero dependiendo del parametro que proporcione el usuario
async def get_clientes_id(id_cliente: int): #ID de tipo entero
    if id_cliente and id_cliente > 0: #Valida que haya ID y que sea mayor a 0
        with sqlite3.connect(ruta) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT id_cliente FROM clientes")
            response = cursor.fetchall()
            respuesta = {'message': 'ID no encontrado'} #Por si no existe
            for i in response:
                if i['id_cliente'] == id_cliente: #Valida que el ID recibido exista en la BD
                    cursor.execute("SELECT * FROM clientes WHERE id_cliente='{}'".format(id_cliente)) 
                    respuesta = cursor.fetchone() #Si es válido envía la consulta de ese registrp
            return respuesta
    else:
        return {'message': 'Número invalido'}

@app.post("/clientes/") #Método para inserciones en BD
async def post_cliente(post_cliente: Post):
    with sqlite3.connect(ruta) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("INSERT INTO clientes (nombre, email) VALUES (?,?);",(post_cliente.nombre, post_cliente.email),)
    return {'mensaje': "Cliente agregado"}

@app.put("/clientes/") #Método para actualizaciones en BD
async def put_cliente(put_cliente: Post):
    with sqlite3.connect(ruta) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("UPDATE clientes SET nombre=?, email=? WHERE id_cliente=?;",(put_cliente.nombre, put_cliente.email, put_cliente.id_cliente),)
    return {'mensaje': "Cliente actualizado"}

@app.delete("/clientes/{id_cliente}")
async def delete_cliente(id_cliente: int):
    with sqlite3.connect(ruta) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente=?;",[id_cliente])
    return {"mensaje":"Cliente borrado"}