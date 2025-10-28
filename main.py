from fastapi import Body, FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

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
    id: int = Field(description='idです')
    name: str = Field(min_length=2, max_length=10)
    age: str = Field(min_length=1)
    gender: str = Field(min_length=1)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "ichiro suzuki",
                "age": "30",
                "gender": "male",
            }
        }
    }

USERS = [
    User(1, 'Jun Ito', '10', 'male'),
    User(2, 'Koji Tanaka', '20', 'female'),
    User(3, 'Taro Yamada', '30', 'male'),
    User(4, 'Hanako Nomura', '40', 'female'),
    User(5, 'David Kim', '50', 'male')
]

@app.get("/user", status_code=status.HTTP_200_OK)
async def read_all_bookds():
    return USERS

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_id(user_id: int = Path(gt=0)):
    for user in USERS:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail='not found')

@app.get("/users/{user_name}", status_code=status.HTTP_200_OK)
async def get_name(user_name: str):
    for user in USERS:
        if user.get('name').casefold() == user_name.casefold():
            return user
        
@app.get("/users/", status_code=status.HTTP_200_OK)
async def get_name_by_query(age: str):
    users_arr = []
    for user in USERS:
        if user.get('age').casefold() == age.casefold():
            users_arr.append(user)
    return users_arr 

@app.get("/users/bygender/", status_code=status.HTTP_200_OK)
async def get_users_by_gender_path(gender: str):
    users_arr = []
    for user in USERS:
        if user.get('gender').casefold() == gender.casefold():
            users_arr.append(user)
    return users_arr

@app.get("/users/{age}/", status_code=status.HTTP_200_OK)
async def get_name_by_query(age: str, gender: str):
    users_arr = []
    for user in USERS:
        if user.get('age').casefold() == age.casefold() and user.get('gender').casefold() == gender.casefold():
            users_arr.append(user)
    return users_arr 

@app.post("/users/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(user_request: UserRequest):
    new_user = User(**user_request.model_dump())
    USERS.append(new_user)
    
@app.put("/users/update_user", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(updated_user=Body()):
    user_changed = False
    for i in range(len(USERS)):
        if USERS[i].get('name').casefold() == updated_user.get('name').casefold():
            USERS[i] = updated_user
            user_changed = True
    if not user_changed:
        raise HTTPException(status_code=404, detail='not found')
    
@app.delete("/users/delete_user/{user_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_name: str):
    for i in range(len(USERS)):
        if USERS[i].get('name').casefold() == user_name.casefold():
            USERS.pop(i)
            break
        
        
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_id(user_id: int = Path(gt=0)):
    user_changed = False
    for i in range(len(USERS)):
        if USERS[i].id == user_id:
            USERS.pop(i)
            user_changed = True
            break
    if not user_changed:
        raise HTTPException(status_code=404, detail='Item not found')