from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
import pyrebase

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

@app.get(
    "/",
    status_code = status.HTTP_202_ACCEPTED,
    summary = "Welcome",
    description = "Welcome"
)
async def hello():
    return { "message" : "Hello World!" }


@app.get(
    "/users/validate",
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
        print(f"ERROR: {error}")
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)


@app.get(
    "/users",
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
        print(f"ERROR: {error}")
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)