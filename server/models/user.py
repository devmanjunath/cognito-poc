from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    email: str

class ConfirmUser(BaseModel):
    username: str
    code: str

class UserSignIn(BaseModel):
    username: str
    password: str

class AttachUser(BaseModel):
    username: str
    groupname: str