from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User, UserDB, Base
from pydantic import BaseModel

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

@app.post("/register/")
async def register_user(user: User, db: Session = Depends(get_db)):
    db_user = UserDB(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login/")
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == login_request.username).first()
    if not user or user.password != login_request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}
