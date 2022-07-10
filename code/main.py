import uvicorn, string

import hashlib  # importa la libreria hashlib
from fastapi import FastAPI
import os
import sqlite3
from typing import List, Optional
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware

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
class Usuarios(BaseModel):
    username: str
    level: int

app = FastAPI()
security = HTTPBasic()
ruta = 'sql/clientes.sqlite'

origins = [
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MÉTODO PARA VALIDAR SI EL USUARIO EXISTE
def get_current_level(credentials: HTTPBasicCredentials = Depends(security)):
    password_b = hashlib.md5(credentials.password.encode())
    password = password_b.hexdigest()
    with sqlite3.connect(ruta) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT level FROM usuarios WHERE username = ? and password = ?",
            (credentials.username, password),
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrecta",
                headers={"WWW-Authenticate": "Basic"},
            )
    return user[0]

@app.get("/", response_model = Respuesta) #Primer endpoint
async def index():
    return {"mensaje": "API REST"}

@app.get("/clientes/",
    response_model=List[Cliente],
    status_code=status.HTTP_202_ACCEPTED ) #Segundo endpoint
async def get_clientes(offset: int = 0, limit: int = 10, level: int = Depends(get_current_level)): #parametros de consulta de tipo entero
    if level == 0 or level == 1:  # Administrador y usuario
        with sqlite3.connect(ruta) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM CLIENTES LIMIT ? OFFSET ?;",(limit, offset),)
            respuesta = cursor.fetchall() #Si es válido envía la consulta de ese registro
            return respuesta
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso.",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/clientes/{id_cliente}",
    status_code=status.HTTP_202_ACCEPTED,) #Ahora como el segundo endpoint pero dependiendo del parametro que proporcione el usuario
async def get_clientes_id(id_cliente: int, level: int = Depends(get_current_level)): #ID de tipo entero
    if level == 0 or level == 1: #Para administradores y usuarios
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
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso.",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.post("/clientes/",
    status_code=status.HTTP_202_ACCEPTED) #Método para inserciones en BD
async def post_cliente(post_cliente: Post, level: int = Depends(get_current_level)):
    if level == 0: #Solo para administradores
        with sqlite3.connect(ruta) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("INSERT INTO clientes (nombre, email) VALUES (?,?);",(post_cliente.nombre, post_cliente.email),)
        return {'mensaje': "Cliente agregado"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso.",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.put("/clientes/",
    status_code=status.HTTP_202_ACCEPTED) #Método para actualizaciones en BD
async def put_cliente(put_cliente: Post, level: int = Depends(get_current_level)):
    if level == 0: #Solo para administradores
        with sqlite3.connect(ruta) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("UPDATE clientes SET nombre=?, email=? WHERE id_cliente=?;",(put_cliente.nombre, put_cliente.email, put_cliente.id_cliente),)
        return {'mensaje': "Cliente actualizado"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso.",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.delete("/clientes/{id_cliente}",
    status_code=status.HTTP_202_ACCEPTED)
async def delete_cliente(id_cliente: int, level: int = Depends(get_current_level)):
    if level == 0: #Solo para administradores
        with sqlite3.connect(ruta) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente=?;",[id_cliente])
        return {"mensaje":"Cliente borrado"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso.",
            headers={"WWW-Authenticate": "Basic"},
        )