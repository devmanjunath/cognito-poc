from fastapi import APIRouter
from server.dal.user import UserConfig
from server.models.user import User, ConfirmUser, UserSignIn, AttachUser

routes = APIRouter()
config = UserConfig()

@routes.post("/sign-up")
def signup(user: User):
    resp = config.user_signup(user.username, user.email, user.password)
    return resp

@routes.post("/confirm-sign-up")
def confirm_signup(user: ConfirmUser):
    resp = config.confirm_signup(user.username, user.code)
    return resp

@routes.post("/sign-in")
def signin(user: UserSignIn):
    resp = config.user_signin(user.username, user.password)
    return resp

@routes.post("/attach-user")
def signin(user: AttachUser):
    resp = config.attach_user_group(user.username, user.groupname)
    return resp