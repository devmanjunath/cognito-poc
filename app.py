from fastapi import FastAPI
from server.endpoints.routes import routers
import uvicorn

app = FastAPI()
app.include_router(routers)

@app.get("/")
def index():
    return {"message": "Welcome to Cognito POC"}

if __name__ == "__main__":
    print("FastAPI is running on 3000")
    uvicorn.run("app:app", host="0.0.0.0", reload=True, port=3000)