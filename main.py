from fastapi import FastAPI

app = FastAPI()

USERS = [
    {'name': 'Jun Ito', 'age': '10', 'gender': 'male'},
    {'name': 'Koji Tanaka', 'age': '20', 'gender': 'female'},
    {'name': 'Taro Yamada', 'age': '30', 'gender': 'male'},
    {'name': 'Hanako Nomura', 'age': '40', 'gender': 'female'},
    {'name': 'David Kim', 'age': '50', 'gender': 'male'},
]

@app.get("/user")
async def read_all_bookds():
    return USERS

@app.get("/users/{user_name}")
async def get_name(user_name: str):
    for user in USERS:
        if user.get('name').casefold() == user_name.casefold():
            return user
        
@app.get("/users/")
async def get_name_by_query(age: str):
    users_arr = []
    for user in USERS:
        if user.get('age').casefold() == age.casefold():
            users_arr.append(user)
    return users_arr 