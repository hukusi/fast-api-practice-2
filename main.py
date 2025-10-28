from fastapi import Body, FastAPI

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

@app.get("/users/bygender/")
async def get_users_by_gender_path(gender: str):
    users_arr = []
    for user in USERS:
        if user.get('gender').casefold() == gender.casefold():
            users_arr.append(user)
    return users_arr

@app.get("/users/{age}/")
async def get_name_by_query(age: str, gender: str):
    users_arr = []
    for user in USERS:
        if user.get('age').casefold() == age.casefold() and user.get('gender').casefold() == gender.casefold():
            users_arr.append(user)
    return users_arr 

@app.post("/users/create_user")
async def create_user(new_user=Body()):
    USERS.append(new_user)
    
@app.put("/users/update_user")
async def update_user(updated_user=Body()):
    for i in range(len(USERS)):
        if USERS[i].get('name').casefold() == updated_user.get('name').casefaold():
            USERS[i] = updated_user
    
@app.delete("/users/delete_user/{user_name}")
async def delete_user(user_name: str):
    for i in range(len(USERS)):
        if USERS[i].get('name').casefold() == user_name.casefold():
            USERS.pop(i)
            break
        
        