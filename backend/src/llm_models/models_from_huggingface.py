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

prompt = input("Include the data u want as a summarizer? ")

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    },
    data= json.dumps({
        "model": "qwen/qwen3-coder:free",
        "messages": [
            {
                "role": "system",
                "content": "Summarize the data which ever u will get in the input. Do include the important points of the data and TLDR of the data which is inlcuded in the prompts"
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
    })
)


print(response.text)


# async def set_context_window(conversation_id: int,DB: AsyncSession = Depends(get_db)):
#     result = await DB.execute(
#         select(Message).where(Message.conversation_id == conversation_id)
#         .order_by(Message.created_at.desc())
#         .limit(10)
#     )
#     history = result.scalars().all()
#     context = list(reversed(history))

#     prompt_messages = [{"role": m.role, "content": m.content} for m in context]
#     return prompt_messages

# ## We need to work on it... still in progress
# async def langchain_llm_mode(user_input, username, conversation_id):
#     response = requests.post(
#         url="https://openrouter.ai/api/v1/chat/completions"
#     )