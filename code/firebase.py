from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
import pyrebase
from pydantic import BaseModel
from requests.exceptions import HTTPError
from fastapi.middleware.cors import CORSMiddleware

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

@app.get(
	"/",
	status_code = status.HTTP_202_ACCEPTED,
	summary = "Welcome",
	description = "Welcome"
)
async def hello():
  	return {"message" : "Hello World!"}


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