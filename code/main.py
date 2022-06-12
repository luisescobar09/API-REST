from fastapi import FastAPI

import sqlite3
from typing import List
from pydantic import BaseModel

class Respuesta(BaseModel): #Modelado de los datos
    mensaje: str
class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str

app = FastAPI()

@app.get("/", response_model = Respuesta) #Primer endpoint
async def index():
    return {"mensaje": "API REST"}

@app.get("/clientes/") #Segundo endpoint
async def clientes(response_model = Cliente):
    with sqlite3.connect('sql/clientes.sqlite') as connection: #Conexión SQLite3
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes") #Consulta todos los registros
        response = cursor.fetchall() #Almacen en una lista
        return response

@app.get("/clientes/{id_cliente}") #Ahora como el segundo endpoint pero dependiendo del parametro que proporcione el usuario
async def clientes(id_cliente: int): #ID de tipo entero
    if id_cliente and id_cliente > 0: #Valida que haya ID y que sea mayor a 0
        with sqlite3.connect('sql/clientes.sqlite') as connection:
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