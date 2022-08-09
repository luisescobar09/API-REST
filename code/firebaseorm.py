from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
import pyrebase
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, create_engine

firebaseConfig = {
	"apiKey": "AIzaSyACOmt65xyc3DocyrTYUT91VLN-6yxmrdI",
	"authDomain": "js-pythonweb.firebaseapp.com",
	"databaseURL": "https://js-pythonweb-default-rtdb.firebaseio.com",
	"projectId": "js-pythonweb",
	"storageBucket": "js-pythonweb.appspot.com",
	"messagingSenderId": "56944178902",
	"appId": "1:56944178902:web:36f92bf2bb8cdbc207bb77",
	"measurementId": "G-28Y64F0CGV"
}

firebase = pyrebase.initialize_app(firebaseConfig)
app = FastAPI()
securityBasic = HTTPBasic()
securityBearer = HTTPBearer()

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

class User(BaseModel):
    email: str
    password: str
class Usuario(BaseModel):
    id_cliente: int
    nombre: str
    email: str
class Post(BaseModel): #Validar los datos de entrada de POST y PUT
    id_cliente: Optional[int]
    nombre: str
    email: str

Base = declarative_base()
engine = create_engine('sqlite:///sql/clientes.sqlite') #CONEXIÓN
#CREACIÓN DEL MODELO (TABLA Y CAMPOS)
class Cliente(Base):
        __tablename__ = 'clientes'

        id_cliente = Column(Integer(), primary_key = True)
        nombre = Column(String(50), nullable = False)
        email = Column(String(50), nullable = False)

        def __str__(self):
                return self.nombre

Session = sessionmaker(engine)
session = Session()

#Insertar
def insert_row(nombre, email):
        try:
                user = Cliente(nombre = nombre, email = email)
                session.add(user)
                session.commit()
                return True
        except Exception as error:
                print(error)
                return False
#Consultar
def query_rows(limit, offset):
        users = session.query(Cliente.id_cliente, Cliente.nombre, Cliente.email).limit(limit).offset(offset)
        if users:
                return [ dict(i) for i in users ]
        else:
                return None
def query_row(id_cliente):
        user = session.query(Cliente.id_cliente, Cliente.nombre, Cliente.email).filter(
                Cliente.id_cliente == id_cliente
        ).first()
        if user:
                return dict(user)
        else:
                return None
#Actualizar
def update_row(id_cliente, nombre, email):
        try:
                session.query(Cliente).filter(
                        Cliente.id_cliente == id_cliente 
                ).update(
                        {
                                Cliente.nombre : nombre,
                                Cliente.email : email
                        }
                )
                session.commit()
                #SEGUNDA FORMA:
                '''user = session.query(Cliente).filter(
                        Cliente.id_cliente == id_cliente
                ).first()
                user.nombre = nombre
                user.email = email
                session.add(user)
                session.commit()'''
                return True
        except Exception as error:
                print(error)
                return False
#Eliminar
def delete_row(id_cliente):
        try:
                session.query(Cliente).filter(
                        Cliente.id_cliente == id_cliente
                ).delete()
                session.commit()
                return True
        except Exception as error:
                print(error)
                return False


# MÉTODO PARA VALIDAR SI EL USUARIO EXISTE
def get_current_level(credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
        try:
                auth = firebase.auth()
                user = auth.get_account_info(credentials.credentials)
                uid = user["users"][0]["localId"]
                db = firebase.database()
                user_data = db.child("users").child(uid).child("level").get().val()
                if user_data:
                        return user_data
                else:
                        raise HTTPException(
                                status_code = 404,
                                detail = "Algo pasó")
        except Exception as error:
                response = str(error)
                if response.count("400") > 0 and response.count("INVALID_ID_TOKEN") > 0:
                        raise HTTPException(
                                status_code = status.HTTP_403_FORBIDDEN,
                                detail = "Token invalido o ya ha caducado.")

@app.get(
	"/",
	status_code = status.HTTP_202_ACCEPTED,
	summary = "Welcome",
	description = "Welcome"
)
async def hello():
  	return { "message" : "Hello World!" }

#################################################### AUTENTICACIÓN 
@app.get(
	"/users/validate/",
	status_code = status.HTTP_202_ACCEPTED,
	summary = "Get a token for a user",
	description = "Get a token for a user",
	tags = ["auth"]
)
async def get_token(credentials: HTTPBasicCredentials = Depends(securityBasic)):
	try:
		email = credentials.username
		password = credentials.password
		auth = firebase.auth()
		user = auth.sign_in_with_email_and_password(email, password)
		response = {
			"token" : user["idToken"]
		}
		return response
	except Exception as error:
		#print(error)
		response = str(error)
		if response.count("400") > 0 and response.count("EMAIL_NOT_FOUND") > 0:
			raise HTTPException(
				status_code = status.HTTP_401_UNAUTHORIZED,
				detail = "Dirección de correo no válido, verifique e intente de nuevo")
		elif response.count("400") > 0 and response.count("INVALID_PASSWORD") > 0:
			raise HTTPException(
				status_code = status.HTTP_401_UNAUTHORIZED,
				detail = "Contraseña incorrecta, verifique e intente de nuevo")
@app.get(
	"/users/",
	status_code = status.HTTP_202_ACCEPTED,
	summary = "Get a user info from token given",
	description = "Get a user info from token given",
	tags = ["auth"]
)
async def get_user(credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
	try:
		auth = firebase.auth()
		user = auth.get_account_info(credentials.credentials)
		uid = user["users"][0]["localId"]
		db = firebase.database()
		user_data = db.child("users").child(uid).get().val()
		response = {
			"user_data" : user_data
		}
		return response

	except Exception as error:
		#print(error)
		response = str(error)
		if response.count("400") > 0 and response.count("INVALID_ID_TOKEN") > 0:
			raise HTTPException(
				status_code = status.HTTP_403_FORBIDDEN,
				detail = "Token invalido o ya ha caducado.")

@app.post(
	"/user/",
	status_code = status.HTTP_201_CREATED, #La solicitud se cumplió, cuyo resultado fue la creación de un nuevo recurso.
	summary = "Create a new account",
	description = "Create a new account",
	tags = ["auth"]
)
async def create_user(post_user : User):
	try:
		auth = firebase.auth()
		creation = auth.create_user_with_email_and_password(post_user.email, post_user.password)
		localId = creation["localId"]
		if localId is not None:
			data = {
				"email" : post_user.email,
				"level" : 1
			}
			db = firebase.database()
			db.child("users").child(localId).set(data)
			return { "response" : "Usuario creado correctamente" }
	except Exception as error:
		response = str(error)
		#print(response)
		if response.count("400") > 0 and response.count("EMAIL_EXISTS") > 0:
			raise HTTPException(
				status_code = status.HTTP_409_CONFLICT,
				detail = "El correo ingresado ya existe, verifique e intente de nuevo")
			'''	HTTP STATUS 409 aplica cuando existe ya un recurso que genera conflicto 
				que no permita completar la solicitud, así queda a la espera de que el
				usuario pueda resolver el problema y vuelva a enviar la solicitud.
			'''
		else:
			raise HTTPException(
				status_code = status.HTTP_401_UNAUTHORIZED,
				detail = "Algo ocurrió")

############## INTERACCIÓN CON LA BASE DE DATOS ########################
@app.get("/clientes/",
        tags = ["database"],
        response_model=List[Usuario],
        status_code=status.HTTP_202_ACCEPTED ) #Segundo endpoint
async def get_clientes(offset: int = 0, limit: int = 10, level: int = Depends(get_current_level)): #parametros de consulta de tipo entero
    if level == 0 or level == 1:  # Administrador y usuario
        response = query_rows(limit= limit, offset= offset)
        if response is not None:
                return response
        else:
                raise HTTPException(
                        status_code= 404,
                        detail="Consulta no encontrada"
                )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso.",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/clientes/{id_cliente}",
        tags = ["database"],
        status_code=status.HTTP_202_ACCEPTED,) #Ahora como el segundo endpoint pero dependiendo del parametro que proporcione el usuario
async def get_clientes_id(id_cliente: int, level: int = Depends(get_current_level)): #ID de tipo entero
    if level == 0 or level == 1: #Para administradores y usuarios
        response = query_row(id_cliente= id_cliente)
        if response is not None:
                return response
        else:
                raise HTTPException(
                        status_code= 404,
                        detail="Consulta no encontrada"
                )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso.",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.post("/clientes/",
        tags = ["database"],
        status_code=status.HTTP_202_ACCEPTED) #Método para inserciones en BD
async def post_cliente(post_cliente: Post, level: int = Depends(get_current_level)):
        if level == 1: #Solo para administradores
                if insert_row(nombre= post_cliente.nombre, email= post_cliente.email) is True:
                        return {'mensaje': "Cliente agregado"}
                else:
                        raise HTTPException(
                                status_code = status.HTTP_409_CONFLICT,
			        detail = "Ocurrió un error al realizar la inserción, verifique e intente más tarde"
                        )   
        else:
                raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="No tienes permiso para acceder a este recurso.",
                        headers={"WWW-Authenticate": "Basic"},
                )

@app.put("/clientes/",
        tags = ["database"],
        status_code=status.HTTP_202_ACCEPTED) #Método para actualizaciones en BD
async def put_cliente(put_cliente: Post, level: int = Depends(get_current_level)):
        if level == 1: #Solo para administradores
                if update_row(id_cliente= put_cliente.id_cliente, nombre= put_cliente.nombre, email= put_cliente.email) is True:
                        return { 'mensaje' : "Cliente actualizado" }
                else:
                        raise HTTPException(
                                status_code = status.HTTP_409_CONFLICT,
                                detail = "Ocurrió un error al realizar la inserción, verifique e intente más tarde"
                        ) 
        else:
                raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a este recurso.",
                headers={"WWW-Authenticate": "Basic"},
                )

@app.delete("/clientes/{id_cliente}",
        tags = ["database"],
        status_code=status.HTTP_202_ACCEPTED)
async def delete_cliente(id_cliente: int, level: int = Depends(get_current_level)):
        if level == 1: #Solo para administradores
                if delete_row(id_cliente= id_cliente) is True:
                        return { "mensaje" : "Cliente borrado" }
                else:
                        raise HTTPException(
                                status_code = status.HTTP_409_CONFLICT,
                                detail = "Ocurrió un error al realizar la eliminación, verifique e intente más tarde"
                        )
        else:
                raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="No tienes permiso para acceder a este recurso.",
                        headers={"WWW-Authenticate": "Basic"},
                )