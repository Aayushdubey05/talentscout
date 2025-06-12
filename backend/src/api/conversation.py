from src.db.db import get_db
from src.db.operations import CRUDBase
from src.models.user import Users, Message, Conversation
from fastapi import APIRouter, HTTPException, status, middleware, Depends, File, UploadFile, Form
from src.schema.user import Reg_of_users
from sqlalchemy import select
from typing import Optional
from src.llm_models.langchain_stuff import extract_pdf_text
from src.middleware.message_role import MessageRole
chat_router= APIRouter()
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from src.llm_models.models_from_huggingface import langchain_llm_mode
@chat_router.get("/chat/{username}",status_code=status.HTTP_200_OK)
async def get_conversation_history(username: str, DB: AsyncSession= Depends(get_db)):
    history = await DB.execute(
        select(Conversation).join(Users).where(Users.username == username).order_by(Conversation.created_at.desc())
    )
    history_of_conversation = history.scalars().all()
    return [{ "conversation_id": hist.id, "title": hist.title, "created_at": hist.created_at} for hist in history_of_conversation]


@chat_router.post("/start-conversation/{username}")
async def start_conversation(username: str = Form(...), conversation_id: int = Form(...), DB: AsyncSession=Depends(get_db), prompt: Optional[str] = Form(None),file : Optional[str] = Form(None)):
    try:
        user = await DB.execute(select(Users).where(Users.username == username))
        user = user.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=404,detail="User not Found")

        new_conversation = await Conversation(user_id=user.id,title = "New Chat")
        if len(new_conversation) is 0:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="You cant send empty messages")
        
        DB.add(new_conversation)
        await DB.commit()
        await DB.refresh(new_conversation)

        return {
            "conversation_id" : new_conversation.id,
            "title" : new_conversation.title
        }
    
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please try again"
        )
    
@chat_router.put("/update-title/{conversation_id}")
async def update_conversation_title(
    conversation_id: int,
    new_title: str,
    DB: AsyncSession= Depends(get_db)
):
    
    result = await DB.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    ) 

    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    
    conversation.title = new_title
    await DB.commit()
    await DB.refresh(conversation)

    return {"message": "title Updated", "new_title": conversation.title}

    
@chat_router.post("/conversations/{conversation_id}/add_message")
async def add_message(
        conversation_id: int,
        role: str,
        content: Optional[str] = Form(None),
        username: Optional[str] = Form(None),
        file: Optional[UploadFile] | None= File(None) ,
        prompt: Optional[str] | None= Form(None),
        DB: AsyncSession = Depends(get_db)
):
    try:
        result = await DB.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )

        conversation = result.scalar_one_or_none()


        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")


        message_content = await extract_pdf_text(file)
        content = message_content + content
        

        # if file:
        #     pdf_content = await extract_pdf_text(file)
        #     content = pdf_content

        # elif prompt:
        #     content = prompt

        # else:
        #     return {"error": "No input provided"}



        new_msg = Message(conversation_id=conversation.id,role=role, content=content,username = username, created_at = datetime.utcnow())
        DB.add(new_msg)
        await DB.commit()
        await DB.refresh(new_msg)

        return {
            "message": "Messages added successfully",
            "message_id": new_msg.id,
            "role": new_msg.role,
            "content": new_msg.content,
            "timestamp": new_msg.created_at
        }
    
    except Exception as e:
        await DB.rollback()
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while adding messages "
        ) 
    

@chat_router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(conversation_id:int, DB: AsyncSession = Depends(get_db)):
    result = await DB.execute(
        select(Message).where(Message.conversation_id ==  conversation_id).order_by(Message.created_at)
    )

    messages = result.scalars().all()

    return [{"role": m.role, "content": m.content, "timestamp": m.created_at} for m in messages ]


# @chat_router.post("/chat")
# async def chat_with_llm(
#     username : str = Form(...),
#     conversation_id : str = Form(...),
#     prompt: Optional[str] = Form(None),
#     file: Optional[UploadFile] = Form(None),
#     DB: AsyncSession = Depends(get_db) 
# ):
    
#     if file:
#         pdf_content = await extract_pdf_text(file)
#         user_input = pdf_content
#     elif prompt:
#         user_input = pdf_content
#     else:
#         return {"error": "No input provided "}
