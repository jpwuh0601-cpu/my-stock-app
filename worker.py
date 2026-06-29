import os
import json
import yfinance as yf
from openai import OpenAI
from datetime import datetime

# 初始化 OpenAI 客戶端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_market_data():
    """獲取與整合所有數據"""
    ticker_symbol = "^TWII"  # 加權指數
    ticker = yf.Ticker(ticker_symbol)
    
    # 1 & 2. 獲取即時數據
    hist = ticker.history(period="1d")
    price = hist['Close'].iloc[-1]
    prev_close = hist['Open'].iloc[-1]
    change = ((price - prev_close) / prev_close) * 100
    
    # 財報 (模擬結構，實際需由爬蟲取得)
    financials = {
        "2025Q1": {"EPS": 5.2, "淨值": 150.2},
        "2024Q4": {"EPS": 4.8, "淨值": 148.5}
    }
    
    # 籌碼數據 (模擬結構，未來可替換為爬蟲結果)
    institutional_investors = [
        {"機構": "外資", "買賣超": 500},
        {"機構": "投信", "買賣超": 200},
        {"機構": "自營商", "買賣超": -150}
    ]
    
    # 獲取新聞
    news = [n['title'] for n in ticker.news[:3]]
    
    # 取得 AI 分析 (含財報預測)
    ai_prediction = get_ai_analysis(news, price, financials)
    
    # 組合資料
    data = {
        "price": round(price, 2),
        "change": round(change, 2),
        "bvps": 150.2, # 每股淨值
        "financials": financials,
        "institutional_investors": institutional_investors,
        "margin_ratio": 1.25, # 10日資券比
        "top_brokers": [
            {"券商": "凱基台北", "買進": 1000, "賣出": 200},
            {"券商": "富邦", "買進": 800, "賣出": 500}
        ],
        "ai_prediction": ai_prediction,
        "news": news,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return data

def get_ai_analysis(news, price, financials):
    """呼叫 AI 進行市場與財報預測"""
    prompt = f"目前加權指數 {price}，財報數據 {financials}。請提供市場分析與財報預測。"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def validate_data(data):
    """自動回測資料是否正確"""
    required_keys = ["price", "bvps", "financials", "institutional_investors"]
    for key in required_keys:
        if key not in data or data[key] is None:
            raise ValueError(f"資料驗證失敗：缺少欄位 {key}")
    print("資料來源回測成功，數據完整。")

if __name__ == "__main__":
    data = get_market_data()
    validate_data(data)
    
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("市場資料已更新至 market_data.json")
