from fastapi import FastAPI

app = FastAPI()

USERS = [
    {'name': 'Jun Ito', 'age': '10歳', 'gender': 'male'},
    {'name': 'Koji Tanaka', 'age': '20歳', 'gender': 'female'},
    {'name': 'Taro Yamada', 'age': '30歳', 'gender': 'male'},
    {'name': 'Hanako Nomura', 'age': '40歳', 'gender': 'female'},
    {'name': 'David Kim', 'age': '50歳', 'gender': 'male'},
]

@app.get("/user")
async def read_all_bookds():
    return USERS

@app.get("/users/{user_name}")
async def get_name(user_name: str):
    for user in USERS:
        if user.get('name').casefold() == user_name.casefold():
            return user