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

# 從環境變數讀取金鑰 (GitHub Actions 與 Streamlit 環境通用)
LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN") or os.getenv("LINE_NOTIFY_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

WATCHLIST = os.getenv("WATCHLIST", "2330,2881,2603,2454").split(",")

# 設定 OpenRouter 客戶端
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENAI_API_KEY
) if OPENAI_API_KEY else None

def log_to_file(message):
    """將分析報告存入本地日誌檔案 (簡易資料庫功能)"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open("daily_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}]\n{message}\n{'-'*30}\n")
    except Exception as e:
        logging.error(f"日誌存檔失敗: {e}")

def get_news(ticker):
    """嘗試使用 Google Search API 獲取最新財經新聞"""
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        return ""
    
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}&q={ticker}+股票+新聞"
    try:
        response = requests.get(url).json()
        items = response.get("items", [])[:2]
        return "\n".join([item['title'] for item in items])
    except:
        return ""

def fetch_stock_data(ticker):
    try:
        stock = twstock.Stock(ticker)
        data = stock.fetch_from(2026, 1)
        df = pd.DataFrame(data)
        
        current_price = df['close'].iloc[-1]
        start_price = df['close'].iloc[0]
        ytd_return = ((current_price - start_price) / start_price) * 100
        
        return {
            "ticker": ticker, 
            "price": current_price, 
            "ytd_return_val": ytd_return, 
            "ytd_return": f"{ytd_return:.2f}%",
            "news": get_news(ticker)
        }
    except Exception as e:
        logging.error(f"數據獲取錯誤: {e}")
        return {"ticker": ticker, "error": "數據異常"}

def get_ai_insight(report_data):
    """透過 OpenRouter 進行進階 AI 深度分析，加入更具體的指令集"""
    if not client:
        return "（未配置 API Key，無法進行深度分析）"
    
    prompt = (
        "請擔任專業投資顧問。請根據以下清單的數據（YTD 報酬與相關新聞）進行深入分析：\n"
        "1. 比較各支股票的績效表現，找出表現最強勢與最弱勢的標的。\n"
        "2. 基於報酬率趨勢，判斷是否出現過度集中或過度發散的風險。\n"
        "3. 綜合新聞資訊，簡要評估這些股票目前是否處於技術超買或超賣區間的觀察點。\n"
        "4. 給出簡潔的投資建議。\n\n"
        f"數據內容: {json.dumps(report_data, ensure_ascii=False)}"
    )
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini", 
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 分析暫時無法使用 (原因: {str(e)[:30]}...)"

def send_line_message(content):
    if not LINE_TOKEN:
        return
        
    # 自動判斷使用 Line Notify 或 Messaging API
    if "notify" in LINE_TOKEN.lower() or len(LINE_TOKEN) < 50:
        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
        payload = {"message": f"\n🤖 AI 決策中樞\n\n{content}"}
    else:
        url = "https://api.line.me/v2/bot/message/broadcast"
        headers = {"Authorization": f"Bearer {LINE_TOKEN}", "Content-Type": "application/json"}
        payload = {"messages": [{"type": "text", "text": f"🤖 AI 決策中樞\n\n{content}"}]}
        
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    report_data = [fetch_stock_data(t) for t in WATCHLIST]
    ai_summary = get_ai_insight(report_data)
    
    # 檢查是否有異常波動
    alerts = []
    for item in report_data:
        if "ytd_return_val" in item and abs(item["ytd_return_val"]) > 5.0:
            alerts.append(f"🚨 異常波動: {item['ticker']} (年報酬 {item['ytd_return']})")
            
    alert_msg = "\n".join(alerts) + "\n\n" if alerts else ""
    
    msg = f"{alert_msg}【績效與盤勢】\n"
    for item in report_data:
        if "error" in item:
            msg += f"- {item['ticker']}: 數據異常\n"
        else:
            msg += f"- {item['ticker']}: 年報酬 {item.get('ytd_return', 'N/A')}\n"
            
    msg += f"\n【AI 深度分析】\n{ai_summary}"
    
    # 發送訊息並同步儲存至資料庫檔案
    send_line_message(msg)
    log_to_file(msg)
