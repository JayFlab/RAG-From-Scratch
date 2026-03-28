import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.openai_like import OpenAILikeEmbedding

# 👇 关键：HyDE
from llama_index.core.indices.query.query_transform.base import HyDEQueryTransform
from llama_index.core.query_engine import TransformQueryEngine


# 1️⃣ 配置模型
Settings.llm = OpenAILike(
    model="qwen-plus",
    api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    is_chat_model=True,
)

Settings.embed_model = OpenAILikeEmbedding(
    model_name="text-embedding-v4",
    api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
)

# 2️⃣ 文档
documents = SimpleDirectoryReader(input_files=["data.txt"]).load_data()

# 3️⃣ 索引
index = VectorStoreIndex.from_documents(documents)

# 4️⃣ 原始 query_engine
query_engine = index.as_query_engine()

# 🔥 5️⃣ 加 HyDE
hyde = HyDEQueryTransform(include_original=True)

query_engine = TransformQueryEngine(
    query_engine,
    query_transform=hyde
)

# 6️⃣ 查询
response = query_engine.query("RAG是什么？")

print(response)