from fastapi import FastAPI
from routers import users

app = FastAPI()

        
@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


app.include_router(users.router)