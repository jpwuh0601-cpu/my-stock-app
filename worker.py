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
# Google 金鑰為非必填，若無則跳過新聞分析
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

WATCHLIST = os.getenv("WATCHLIST", "2330,2881,2603,2454").split(",")

client = OpenAI(api_key=OPENAI_API_KEY)

def get_news(ticker):
    """嘗試使用 Google Search API 獲取最新財經新聞，若金鑰不存在則跳過"""
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        return "（未配置新聞搜尋功能）"
    
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}&q={ticker}+股票+新聞"
    try:
        response = requests.get(url).json()
        items = response.get("items", [])[:3]
        if not items:
            return "目前無相關新聞。"
        return "\n".join([item['title'] for item in items])
    except Exception as e:
        logging.error(f"新聞獲取失敗: {e}")
        return "無法獲取新聞。"

def fetch_stock_data(ticker):
    try:
        stock = twstock.Stock(ticker)
        data = stock.fetch_from(2026, 1) # 從年初開始
        df = pd.DataFrame(data)
        
        current_price = df['close'].iloc[-1]
        start_price = df['close'].iloc[0]
        ytd_return = ((current_price - start_price) / start_price) * 100
        
        return {
            "ticker": ticker, 
            "price": current_price, 
            "ytd_return": f"{ytd_return:.2f}%",
            "news": get_news(ticker)
        }
    except Exception as e:
        logging.error(f"數據獲取錯誤: {e}")
        return {"ticker": ticker, "error": "數據異常"}

def get_ai_insight(report_data):
    # 根據現有資料生成分析提示詞
    prompt = f"分析以下股市數據 (YTD 報酬率與相關資訊)，給出專業投資觀點: {json.dumps(report_data, ensure_ascii=False)}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"AI 分析失敗: {e}")
        return "AI 分析服務暫時無法取得。"

def send_line_message(content):
    if not LINE_TOKEN:
        logging.warning("未設定 LINE_CHANNEL_ACCESS_TOKEN，跳過發送。")
        return
        
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}", "Content-Type": "application/json"}
    payload = {"messages": [{"type": "text", "text": f"🤖 AI 決策中樞\n\n{content}"}]}
    
    try:
        requests.post(url, headers=headers, json=payload)
        logging.info("LINE 訊息發送成功。")
    except Exception as e:
        logging.error(f"LINE 發送失敗: {e}")

if __name__ == "__main__":
    report_data = [fetch_stock_data(t) for t in WATCHLIST]
    ai_summary = get_ai_insight(report_data)
    
    msg = "【績效與盤勢】\n"
    for item in report_data:
        if "error" in item:
            msg += f"- {item['ticker']}: 數據異常\n"
        else:
            msg += f"- {item['ticker']}: 年報酬 {item.get('ytd_return', 'N/A')}\n"
            
    msg += f"\n【AI 深度分析】\n{ai_summary}"
    send_line_message(msg)
