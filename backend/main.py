from fastapi import FastAPI, Response, HTTPException, Depends
from database import get_session, engine, SessionDep
import uvicorn
from models import User
from schemas import UserCreate
from sqlalchemy.future import select
from passlib.context import CryptContext
from schemas import UserLogin, UserResponse
from authx import AuthXConfig, AuthX

config_jwt = AuthXConfig()

config_jwt.JWT_SECRET_KEY = 'secret'
config_jwt.JWT_ACCESS_COOKIE_NAME = 'access_token'
config_jwt.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config_jwt)
app = FastAPI(
    title="FastAPI SQLAlchemy Async",
    description="FastAPI + SQLAlchemy Async = ❤️",
    version="0.1.0"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/register/', tags=["Authorization🔒"], response_model=UserCreate)
async def register_user(user: UserCreate, session: SessionDep):
    result = await session.execute(select(User).where(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        username=user.username,
        name=user.name,
        email=user.email,
        password=hashed_password,
        skills=user.skills,
        interests=user.interests,
        bio=user.bio,
        location=user.location,
        age=user.age,
        gender=user.gender
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return UserResponse.model_validate(new_user)

@app.post('/auth/', tags=["Authorization🔒"])
async def login_user(cred: UserLogin, session: SessionDep, response: Response):
    result = await session.execute(select(User).where(User.username == cred.username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not pwd_context.verify(cred.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = security.create_access_token(uid=str(user.id))
    response.set_cookie(key=config_jwt.JWT_ACCESS_COOKIE_NAME, value=token, httponly=True)
    return {"access_token": token}


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)