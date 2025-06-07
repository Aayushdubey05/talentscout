from src.core.settings import settings
from src.db.db import get_db,Base
from sqlalchemy import Integer, Column, String, DateTime, Text, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,index=True)
    username = Column(String, unique=True,index=True)
    email = Column(String, unique=True,index=True)
    password = Column(String)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

    conversations = relationship("Conversation",back_populates="user")

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    title = Column(String,default="New chat")
    model_name = Column(String) # I think I dont need this so I will remove it if I dont use it 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("Users",back_populates="conversations")
    messages = relationship("Message",back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer,primary_key=True,index = True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String)
    content = Column(Text)
    model_name = Column(String,nullable=True)
    token_used = Column(String,nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    conversation = relationship("Conversation",back_populates="messages")


