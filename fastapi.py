from dashscope_config import require_dashscope_api_key

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

api_key = require_dashscope_api_key()


#初始化对应的服务对象
client = OpenAI(
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

class ChatRequest(BaseModel):
    query:str
    top_k:int = 3

@app.get("/")
def home():
    return {"message":"fastapi后端启动成功"}

@app.post("/chat")
def chat(request:ChatRequest):
    User_query = request.query
    top_k = request.top_k

    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role":"user","content": request.query}
        ]
    )
    answer = response.choices[0].message.content
    return { 
            "answer":answer
           }

@app.get("/ping")
def ping():
    return {"status": "ok"}