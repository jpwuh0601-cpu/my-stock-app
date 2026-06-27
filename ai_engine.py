import openai
import os

# 初始化 OpenAI Client
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_ai_summary(data):
    """將財務指標轉交給 GPT 分析"""
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
            model="gpt-4o",
            messages=[{"role": "system", "content": "你是一位專業的台股投資分析師。"},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 分析暫時無法取得: {e}"
