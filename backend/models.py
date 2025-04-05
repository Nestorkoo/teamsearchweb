from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Text

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)
    skills = Column(String)
    interests = Column(String)
    bio = Column(String)
    location = Column(String)
    age = Column(Integer)
    gender = Column(String)
    messages = relationship("Message", back_populates="user")
    posts = relationship("PostSearch", back_populates="creator")

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text)

    user = relationship("User", back_populates="messages")
    
class PostSearch(Base):
    __tablename__ = 'post_search'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    location = Column(String(100))
    skills = Column(Text)
    interests = Column(Text)
    creator_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="posts")
    
