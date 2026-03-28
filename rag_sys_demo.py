from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


#==============================================
#RAG的离线处理部分
#create object
loader = TextLoader("data.txt",encoding="utf-8")
documents = loader.load()

#chunk
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap =20
)

docs = splitter.split_documents(documents)

#embedding
embeddings = OpenAIEmbeddings(
    model="text-embedding-v4",
    api_key = "sk-ec67bb0bcfea4afab1740cc5d83a7c81",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    check_embedding_ctx_length=False,
    chunk_size=10
)

#database
db = FAISS.from_documents(docs,embeddings)

#检索到最相似的两个内容
#for r in results:
#   print(r.page_content)
#=========================================================================

#==========================================================
#langchian工作流的部分
#prompt

prompt = ChatPromptTemplate.from_template(
    """请根据上下文回答相应的问题，没有的内容请回复“没有”。
上下文：{context}

问题：{question}
"""
)

#model
model = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-ec67bb0bcfea4afab1740cc5d83a7c81"
)

#response
response = StrOutputParser()

chain = prompt|model|response

class ChatRequest(BaseModel):
    question:str

app = FastAPI()
@app.post("/chat")
def chat(request:ChatRequest):
    
    #换成 LlamaIndex 后
    #=======================================================
    query = request.question
    results = db.similarity_search(query,k=2) #检索的结果
    # 拼接上下文
    context = "\n".join([r.page_content for r in results])
    #=======================================================
    



    #业务逻辑和接口逻辑一定要分开，后面写fastapi一定要注意
    answer = chain.invoke({
    "context":context,
    "question":query
    })
    return {
        "query":query,
        "context":context,
        "answer":answer
    }
    