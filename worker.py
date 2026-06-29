import os
from openai import OpenAI

# 修改這一段，告訴程式使用 OpenRouter 的網址
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)
```

### 為什麼這樣做會成功？
1. **`base_url`**：這行程式碼強制把連線目的地從 OpenAI 轉向 OpenRouter。
2. **`api_key`**：這行指定使用您在 `main.yml` 中設定的 `OPENROUTER_API_KEY` 環境變數。

### 下一步動作：
1. 更新 `worker.py` 中的程式碼。
2. 檢查 GitHub 的 **Settings > Secrets and variables > Actions**，確認裡面確實已經新增了 `OPENROUTER_API_KEY` 這個變數（如果之前只有 OpenAI 的，記得要新增這一個）。
3. 推送您的更新到 GitHub，這樣 Python 程式就會正確連線到 OpenRouter 了！

這樣修改後，應該就能順利繞過 OpenAI 的額度限制了！如果修改後還有問題，請隨時告訴我。
