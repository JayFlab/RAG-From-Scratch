from dashscope_config import require_dashscope_api_key

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

api_key = require_dashscope_api_key()


#prompt
prompt = ChatPromptTemplate.from_template(
    "请回答以下问题：{question}"
)
    
#model
model = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=api_key
)

#output
response = StrOutputParser()

chain = prompt|model|response

app = FastAPI()

class ChatRequest(BaseModel):
    question:str

@app.post("/chat")
def chat(request:ChatRequest):
    answer = chain.invoke({"question":request.question})     
    return {"answer":answer}
