import os
import requests
import twstock
import pandas as pd
import logging
import json
from datetime import datetime
from openai import OpenAI

# 設定日誌紀錄格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 從環境變數讀取金鑰
LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

WATCHLIST = os.getenv("WATCHLIST", "2330,2881,2603,2454").split(",")

client = OpenAI(api_key=OPENAI_API_KEY)

def get_news(ticker):
    """使用 Google Search API 獲取新聞"""
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        return "未設定搜尋 API 金鑰，跳過新聞分析。"
    
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}&q={ticker}+股票+新聞"
    try:
        response = requests.get(url).json()
        items = response.get("items", [])[:3]
        return "\n".join([item['title'] for item in items])
    except:
        return "無法獲取最新新聞。"

def fetch_stock_data(ticker):
    try:
        stock = twstock.Stock(ticker)
        data = stock.fetch_from(2026, 1) # 從年初開始
        df = pd.DataFrame(data)
        
        current_price = df['close'].iloc[-1]
        start_price = df['close'].iloc[0]
        ytd_return = ((current_price - start_price) / start_price) * 100
        
        change_pct = ((df['close'].iloc[-1] - df['close'].iloc[-2]) / df['close'].iloc[-2]) * 100
        
        return {
            "ticker": ticker, 
            "price": current_price, 
            "ytd_return": f"{ytd_return:.2f}%",
            "change": f"{change_pct:.2f}%",
            "news": get_news(ticker)
        }
    except Exception as e:
        logging.error(f"數據獲取錯誤: {e}")
        return {"ticker": ticker, "error": "數據異常"}

def get_ai_insight(report_data):
    prompt = f"分析以下股市數據與新聞，給出投資觀點: {json.dumps(report_data, ensure_ascii=False)}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def send_line_message(content):
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}", "Content-Type": "application/json"}
    payload = {"messages": [{"type": "text", "text": f"🤖 AI 決策中樞\n\n{content}"}]}
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    report_data = [fetch_stock_data(t) for t in WATCHLIST]
    ai_summary = get_ai_insight(report_data)
    
    msg = "【績效與盤勢】\n"
    for item in report_data:
        msg += f"- {item['ticker']}: 年報酬 {item.get('ytd_return', 'N/A')}\n"
    msg += f"\n【AI 深度分析】\n{ai_summary}"
    send_line_message(msg)
