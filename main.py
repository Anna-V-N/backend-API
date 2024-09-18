from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crud import create_user, get_user, update_user, deactivate_user
from database import init_db

app = FastAPI()

# init DB
@app.on_event("startup")
def on_startup():
    init_db()

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str

class UserUpdate(BaseModel):
    username: str = None
    email: str = None
    full_name: str = None

# make user
@app.post("/users/")
def create_user_endpoint(user: UserCreate):
    try:
        create_user(user.username, user.email, user.full_name)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# make user ID
@app.get("/users/{user_id}")
def get_user_endpoint(user_id: int):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user)

# update user ID
@app.put("/users/{user_id}")
def update_user_endpoint(user_id: int, user: UserUpdate):
    update_user(user_id, user.username, user.email, user.full_name)
    return {"message": "User updated successfully"}

# delete user
@app.delete("/users/{user_id}")
def deactivate_user_endpoint(user_id: int):
    deactivate_user(user_id)
    return {"message": "User deactivated successfully"}
