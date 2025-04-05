from fastapi import FastAPI, Response, HTTPException, Depends
from database import SessionDep
import uvicorn
from models import UserModel
from schemas import UserCreate
from sqlalchemy.future import select
from config import config_jwt, security
from passlib.context import CryptContext
from schemas import UserLogin, UserResponse
from authx import AuthXConfig, AuthX
from deps import get_current_user_id
import logging
from fastapi.middleware.cors import CORSMiddleware






app = FastAPI(
    title="FastAPI SQLAlchemy Async",
    description="FastAPI + SQLAlchemy Async = ❤️",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/register/', tags=["Authorization🔒"], response_model=UserResponse)
async def register_user(user_data: UserCreate, db_session: SessionDep):
    try:
        user_query = await db_session.execute(select(UserModel).where(UserModel.email == user_data.email))
        existing_user = user_query.scalars().first()
        if existing_user is not None:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = pwd_context.hash(user_data.password)

        new_user = UserModel(
            username=user_data.username,
            name=user_data.name,
            email=user_data.email,
            password=hashed_password,
            skills=user_data.skills,
            interests=user_data.interests,
            bio=user_data.bio,
            location=user_data.location,
            age=user_data.age,
            gender=user_data.gender
        )
        db_session.add(new_user)
        await db_session.commit()
        await db_session.refresh(new_user)
        return UserResponse.model_validate(new_user)
    except Exception as e:
        logging.error(f"Error during user registration: {e}")
        await db_session.rollback()
        raise HTTPException(status_code=500, detail="An error occurred during registration") from e

@app.post("/auth/", tags=["Authorization🔒"])
async def authenticate_user(credentials: UserLogin, db_session: SessionDep, response: Response):
    """Authenticate a user by username and password and return an access token."""
    try:
        user_query = await db_session.execute(select(UserModel).where(UserModel.username == credentials.username))
        user = user_query.scalars().first()
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        if not pwd_context.verify(credentials.password, user.password):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        token = security.create_access_token(uid=str(user.id))
        response.set_cookie(
            key=config_jwt.JWT_ACCESS_COOKIE_NAME,
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
        )
        return {"access_token": token, "user_id": user.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during authentication") from e

@app.get('/user/<int:user_id>', tags=["User"], dependencies=[Depends(security.access_token_required)])
async def get_user(user_id: int, db_session: SessionDep):
    try:
        user_query = await db_session.execute(select(UserModel).where(UserModel.id == user_id))
        user = user_query.scalars().first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during user retrieval") from e

@app.get('/users/', tags=["User"], dependencies=[Depends(security.access_token_required)])
async def get_users(db_session: SessionDep):
    try:
        users_query = await db_session.execute(select(UserModel))
        users = users_query.scalars().all()
        return [UserResponse.model_validate(user) for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during user retrieval") from e
    

@app.delete('/delete_account/', tags=["Profile"], dependencies=[Depends(security.access_token_required)])
async def delete_account(
    user_id: int, 
    db_session: SessionDep, 
    current_user_id: int = Depends(get_current_user_id)
):
    logging.info(f"Deleting account for user_id: {user_id}, current_user_id: {current_user_id}")
    """Delete the account if the user is the owner."""
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own account")
    
    try:
        user_query = await db_session.execute(select(UserModel).where(UserModel.id == user_id))
        user = user_query.scalars().first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        await db_session.delete(user)
        await db_session.commit()
        return {"message": "Account deleted successfully"}
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(status_code=500, detail="An error occurred during account deletion") from e

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
