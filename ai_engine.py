import openai
import os

# 初始化 OpenAI Client，透過 base_url 對接 OpenRouter
# 請確保您的 Streamlit Secrets 中的金鑰名稱為 OPENROUTER_API_KEY
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY") 
)

def get_ai_summary(data):
    """將財務指標轉交給 GPT 分析 (經由 OpenRouter 路由)"""
    prompt = f"""
    請針對這檔台股資料進行分析：
    {data}
    請提供：
    1. 短期技術面建議
    2. 基本面總結 (本益比與淨值評估)
    3. 給予一個「買進」、「賣出」或「觀望」的 AI 評級與理由。
    """
    
    try:
        response = client.chat.completions.create(
            # 使用 OpenRouter 支援的模型 (例如 Llama-3 或 GPT-4)
            model="meta-llama/llama-3-8b-instruct",
            messages=[
                {"role": "system", "content": "你是一位專業的台股投資分析師。請用繁體中文回答。"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 分析發生錯誤: {e}"
