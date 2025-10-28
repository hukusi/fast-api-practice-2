from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class User:
    id: int
    name: str
    age: str
    gender: str
    
    def __init__(self, id, name, age, gender):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender

class UserRequest(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=10)
    age: str = Field(min_length=1)
    gender: str = Field(min_length=1)

USERS = [
    User(1, 'Jun Ito', '10', 'male'),
    User(2, 'Koji Tanaka', '20', 'female'),
    User(3, 'Taro Yamada', '30', 'male'),
    User(4, 'Hanako Nomura', '40', 'female'),
    User(5, 'David Kim', '50', 'male')
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
async def create_user(user_request: UserRequest):
    new_user = User(**user_request.model_dump())
    USERS.append(new_user)
    
@app.put("/users/update_user")
async def update_user(updated_user=Body()):
    for i in range(len(USERS)):
        if USERS[i].get('name').casefold() == updated_user.get('name').casefold():
            USERS[i] = updated_user
    
@app.delete("/users/delete_user/{user_name}")
async def delete_user(user_name: str):
    for i in range(len(USERS)):
        if USERS[i].get('name').casefold() == user_name.casefold():
            USERS.pop(i)
            break
        
        