import os
from openai import OpenAI

# 初始化客戶端，這裡使用環境變數 OPENAI_API_KEY
# 請確保 GitHub Actions 環境變數設定正確
client = OpenAI(
    base_url="[https://openrouter.ai/api/v1](https://openrouter.ai/api/v1)",
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# 以下是您原本的業務邏輯...
