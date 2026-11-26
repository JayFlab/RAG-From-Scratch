from dashscope_config import require_dashscope_api_key

from openai import OpenAI

api_key = require_dashscope_api_key()


client = OpenAI(
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你能做些什么？"},
    ]
)
print(completion.choices[0].message.content)