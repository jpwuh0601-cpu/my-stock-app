import os
import json
import yfinance as yf
from openai import OpenAI
from datetime import datetime

# 將 OpenAI client 指向 OpenRouter
# 請確保您的 OPENAI_API_KEY 環境變數中儲存的是 OpenRouter 的 Key
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)

def get_ai_analysis(news, price, financials):
    """使用 OpenRouter 進行分析"""
    try:
        prompt = f"目前加權指數 {price}，財報數據 {financials}。請提供市場分析與財報預測。"
        response = client.chat.completions.create(
            # 使用 OpenRouter 支援的模型名稱 (例如 google/gemini-2.0-flash-lite)
            model="google/gemini-2.0-flash-lite", 
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 分析暫時無法取得 (錯誤: {str(e)})"

def get_market_data():
    """獲取並整合數據"""
    ticker = yf.Ticker("^TWII")
    hist = ticker.history(period="1d")
    price = hist['Close'].iloc[-1]
    change = ((price - hist['Open'].iloc[-1]) / hist['Open'].iloc[-1]) * 100
    
    data = {
        "price": round(float(price), 2),
        "change": round(float(change), 2),
        "bvps": 150.2,
        "financials": {"2025Q1": {"EPS": 5.2, "淨值": 150.2}, "2024Q4": {"EPS": 4.8, "淨值": 148.5}},
        "institutional_investors": [{"機構": "外資", "買賣超": 500}, {"機構": "投信", "買賣超": 200}],
        "margin_ratio": 1.25,
        "top_brokers": [{"券商": "凱基台北", "買進": 1000, "賣出": 200}],
        "ai_prediction": get_ai_analysis("最新新聞", price, "財報數據"),
        "news": [n['title'] for n in ticker.news[:3]]
    }
    return data

if __name__ == "__main__":
    data = get_market_data()
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
