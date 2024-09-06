from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

# Configuration de la base de données SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modèle utilisateur avec e-mail comme clé primaire
class UserDB(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True, index=True)  # Utilisation de l'email comme clé primaire
    password = Column(String)
    is_admin = Column(Boolean, default=False)  # Booléen pour déterminer si l'utilisateur est admin ou non

Base.metadata.create_all(bind=engine)

# Modèle de données pour l'utilisateur
class User(BaseModel):
    email: str
    password: str
    is_admin: bool = False

# Dépendance pour obtenir la session de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint pour l'enregistrement des utilisateurs
@app.post("/register")
def register(user: User, db: Session = Depends(get_db)):
    if db.query(UserDB).filter(UserDB.email == user.email).first():
        raise HTTPException(status_code=400, detail="User already exists")
    db_user = UserDB(email=user.email, password=user.password, is_admin=user.is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully", "user_email": db_user.email}

# Endpoint pour la connexion des utilisateurs
@app.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password != password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    if user.is_admin:
        return {"message": "Admin login successful"}
    return {"message": "User login successful"}

# Endpoint pour supprimer un utilisateur
@app.delete("/delete")
def delete_user(email: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
