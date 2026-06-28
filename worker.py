import os
import requests
import yfinance as yf
from openai import OpenAI
from datetime import datetime

# 初始化
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def get_ai_financial_analysis(news_list, info):
    """結合新聞與財務指標進行深度分析"""
    if not client:
        return "⚠️ OpenAI API Key 未設定。"
    
    # 提取財務指標
    pe = info.get('trailingPE', 'N/A')
    yield_rate = info.get('dividendYield', 0) * 100
    
    prompt = f"""
    請擔任專業分析師，綜合以下資料對台股進行觀點分析：
    - 新聞重點：{news_list}
    - 財務指標：本益比(PE)約 {pe}, 殖利率約 {yield_rate}%
    
    請分析：這些財務指標結合新聞面，對市場是正面還是負面？並給出投資建議。
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"分析錯誤: {e}"

def run_smart_report():
    try:
        ticker = yf.Ticker("^TWII")
        # 抓取基本面數據
        info = ticker.info
        news = ticker.news
        news_str = "\n".join([n.get('title', '') for n in news[:3]])
        
        # 進行結合指標的 AI 分析
        analysis = get_ai_financial_analysis(news_str, info)
        
        # 發送至 LINE
        token = os.getenv("LINE_NOTIFY_TOKEN")
        if token:
            msg = (f"\n📈 AI 深度決策晨報 ({datetime.now().strftime('%Y-%m-%d')})\n\n"
                   f"【基本面指標】: 本益比 {info.get('trailingPE', 'N/A')}\n"
                   f"【AI 決策建議】:\n{analysis}")
            requests.post("https://notify-api.line.me/api/notify", 
                          headers={"Authorization": f"Bearer {token}"}, 
                          data={"message": msg})
    except Exception as e:
        print(f"任務錯誤: {e}")

if __name__ == "__main__":
    run_smart_report()
