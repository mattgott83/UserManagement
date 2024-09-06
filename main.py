from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Un modèle de données pour les utilisateurs
class User(BaseModel):
    username: str
    email: str
    password: str

# Une base de données fictive pour stocker les utilisateurs
users_db = {}

# Endpoint pour l'enregistrement des utilisateurs
@app.post("/register")
async def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.username] = user
    return {"message": "User registered successfully"}

# Endpoint pour la connexion des utilisateurs
@app.post("/login")
async def login(username: str, password: str):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user = users_db[username]
    if user.password != password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {"message": "Login successful"}

# Endpoint pour supprimer un utilisateur
@app.delete("/delete")
async def delete_user(username: str):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[username]
    return {"message": "User deleted successfully"}
