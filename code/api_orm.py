from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert, select, update, delete
from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, status
import databases, sqlalchemy

path = 'sqlite:///sql/clientes.sqlite'
engine = create_engine(path)
app = FastAPI()
database = databases.Database(path)

metadata = MetaData()
clientes = Table(
  'clientes', metadata,
  Column( 'id_cliente', Integer, primary_key = True),
  Column( 'nombre', String, nullable = False ),
  Column( 'email', String, nullable = False )
)
metadata.create_all(engine)

class Cliente(BaseModel):
	id_cliente: int
	nombre: str
	email: str

class ClienteIN(BaseModel):
	nombre : str
	email: str

class Message(BaseModel):
	message : str

@app.get(
	"/",
	status_code = status.HTTP_202_ACCEPTED,
	summary = "Welcome",
	description = "Welcome"
)
async def hello():
  	return { "message" : "Hello World!" }

@app.post(
	"/clientes",
	status_code = status.HTTP_202_ACCEPTED,
	summary = "Insert",
	description = "Insert",
	response_model = Message
)
async def post_cliente(post_cliente: ClienteIN):
	nombre= post_cliente.nombre
	email= post_cliente.email
	query = insert(clientes).values(nombre=nombre, email=email)
	await database.execute(query)
	return { 'message': "Cliente agregado correctamente." }


@app.get(
	"/clientes",
	status_code = status.HTTP_202_ACCEPTED,
	summary = "Query",
	description = "Query",
	response_model = List[Cliente]
)
async def get_clientes():
	query = select(clientes)
	return await database.fetch_all(query)

@app.get(
	"/clientes/{id_cliente}",
	status_code = status.HTTP_202_ACCEPTED,
	summary = "Query",
	description = "Query",
	response_model = Cliente
)
async def get_clientes_id( id_cliente: int ):
	query = select(clientes).where(clientes.c.id_cliente == id_cliente)
	return await database.fetch_one(query)
	

@app.put(
	"/clientes",
	status_code = status.HTTP_202_ACCEPTED,
	summary = "Update",
	description = "Update",
	response_model = Message
)
async def put_cliente(put_cliente: Cliente):
	id_cliente = put_cliente.id_cliente
	nombre = put_cliente.nombre
	email = put_cliente.email
	query = update(clientes).where(clientes.c.id_cliente == id_cliente).values(nombre = nombre, email = email)
	await database.execute(query)
	return { 'message': "Cliente actualizado correctamente." }

@app.delete(
	"/clientes/{id_cliente}",
	status_code = status.HTTP_202_ACCEPTED,
	summary = "Delete",
	description = "Delete",
	response_model = Message
)
async def delete_cliente( id_cliente: int ):
	query = delete(clientes).where(clientes.c.id_cliente == id_cliente)
	await database.execute(query)
	return { 'message' : 'Cliente eliminado correctamente.' }
