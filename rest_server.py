from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Mock data
USERS = [
    {"id": i, "name": f"User {i}", "email": f"user{i}@example.com",
     "phone": f"555-000{i}", "address": f"{i} Main St", "city": "CityX",
     "country": "CountryX", "age": 20 + i}
    for i in range(1, 101)
]

class User(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    address: str
    city: str
    country: str
    age: int

@app.get("/user/{user_id}", response_model=User)
def get_user(user_id: int):
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users", response_model=List[User])
def list_users(limit: int = 10):
    return USERS[:limit]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
