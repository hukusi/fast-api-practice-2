from fastapi import FastAPI
from routers import auth, notes, users

app = FastAPI()

        
@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(notes.router)