from fastapi import FastAPI
import uvicorn
from user import User, ConfirmUser, UserSignIn
from UserDal import UserConfig
from S3Dal import S3Config

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Welcome to Cognito POC"}

@app.post("/sign-up")
def signup(user: User):
    config = UserConfig()
    resp = config.user_signup(user.username, user.email, user.password)
    return resp

@app.post("/confirm-sign-up")
def confirm_signup(user: ConfirmUser):
    config = UserConfig()
    resp = config.confirm_signup(user.username, user.code)
    return resp

@app.post("/sign-in")
def signin(user: UserSignIn):
    config = UserConfig()
    resp = config.user_signin(user.username, user.password)
    return resp

@app.get("/s3")
def signin():
    config = S3Config()
    resp = config.list_buckets()
    return resp

if __name__ == "__main__":
    print("FastAPI is running on 3000")
    uvicorn.run("app:app", host="0.0.0.0", reload=True, port=3000)