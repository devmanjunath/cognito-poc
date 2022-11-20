from fastapi import APIRouter
from server.dal.s3 import S3Config

routes = APIRouter()
config = S3Config()

@routes.get("/s3")
def signin():
    resp = config.list_buckets()
    return resp
