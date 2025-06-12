from src.db.db import get_db
from src.models.user import Users,Message,Conversation
from src.schema.user import Reg_of_users,Non_reg_users
from src.ocr.ocrtools import extract_resume_test, conversion_of_text_to_json
import json 
import requests
from langchain.llms.base import LLM
from src.core.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from sqlalchemy import select

prompt = input("Enter about your experince coding background and techstack you work on ")

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    },
    data= json.dumps({
        "model": "sarvamai/sarvam-m:free",
        "messages": [
            {
                "role": "system",
                "content": "You are a highly experienced technical interviewer with 30 years of experience. Ask one coding question at a time. along with that also ask core concepts of engineering related to DBMS and OS do include advance concept if user has 4+ years of experience + question on the techstack user have metioned "
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
    })
)


print(response.text)


async def set_context_window(conversation_id: int,DB: AsyncSession = Depends(get_db)):
    result = await DB.execute(
        select(Message).where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(10)
    )
    history = result.scalars().all()
    context = list(reversed(history))

    prompt_messages = [{"role": m.role, "content": m.content} for m in context]
    return prompt_messages

async def langchain_llm_mode(user_input, username, conversation_id):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions"
    )