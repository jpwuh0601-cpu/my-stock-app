import os
import requests
import twstock
import pandas as pd
import logging
import json
import random
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
    """將分析報告存入本地日誌檔案"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open("daily_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}]\n{message}\n{'-'*30}\n")
    except Exception as e:
        logging.error(f"日誌存檔失敗: {e}")

def get_fundamental_data(ticker):
    """模擬獲取個股基本面數據 (EPS/PE)，實際應用可串接 Yahoo Finance API"""
    # 這裡模擬回傳數值，實際生產環境建議改用 yfinance 套件
    return {
        "EPS": round(random.uniform(5, 30), 2),
        "PE_Ratio": round(random.uniform(10, 30), 2)
    }

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
        
        # 計算 RSI (14日)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs.iloc[-1]))
        
        # 加入基本面數據
        fundamentals = get_fundamental_data(ticker)
        
        return {
            "ticker": ticker, 
            "price": current_price, 
            "ytd_return_val": ytd_return, 
            "ytd_return": f"{ytd_return:.2f}%",
            "rsi": f"{rsi:.2f}",
            "eps": fundamentals["EPS"],
            "pe": fundamentals["PE_Ratio"],
            "news": get_news(ticker)
        }
    except Exception as e:
        logging.error(f"數據獲取錯誤: {e}")
        return {"ticker": ticker, "error": "數據異常"}

def get_ai_insight(report_data):
    """透過 OpenRouter 進行進階 AI 深度分析，包含基本面與技術面"""
    if not client:
        return "（未配置 API Key，無法進行深度分析）"
    
    prompt = (
        "請擔任專業投資顧問。請根據以下數據（包含 RSI 指標、EPS/PE 基本面與新聞）進行綜合評估：\n"
        "1. RSI > 70 代表超買，RSI < 30 代表超賣。\n"
        "2. 結合 PE 與 EPS 判斷個股估值是否合理。\n"
        "3. 比較績效表現與技術指標，給出短線調整建議。\n"
        "4. 給出簡潔的投資總結。\n\n"
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
        
    if "notify" in LINE_TOKEN.lower() or len(LINE_TOKEN) < 50:
        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
        payload = {"message": f"\n{content}"}
    else:
        url = "https://api.line.me/v2/bot/message/broadcast"
        headers = {"Authorization": f"Bearer {LINE_TOKEN}", "Content-Type": "application/json"}
        payload = {"messages": [{"type": "text", "text": content}]}
        
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    try:
        report_data = [fetch_stock_data(t) for t in WATCHLIST]
        ai_summary = get_ai_insight(report_data)
        
        alerts = []
        for item in report_data:
            if "ytd_return_val" in item and abs(item["ytd_return_val"]) > 5.0:
                alerts.append(f"🚨 異常: {item['ticker']} 波動達 {item['ytd_return']}")
                
        alert_msg = " | ".join(alerts) + "\n\n" if alerts else ""
        
        msg = f"🤖 AI 決策中樞報告\n{'-'*15}\n{alert_msg}"
        for item in report_data:
            if "error" not in item:
                msg += f"📌 {item['ticker']}\n- 報酬: {item['ytd_return']}\n- RSI: {item['rsi']}\n- EPS/PE: {item['eps']}/{item['pe']}\n\n"
                
        msg += f"🧠 深度觀點\n{ai_summary}"
        
        send_line_message(msg)
        log_to_file(msg)
    except Exception as e:
        # 當主程序失敗時，嘗試發送錯誤通知給 LINE
        send_line_message(f"❌ 系統錯誤: 自動化任務執行失敗，請檢查 GitHub Actions。\n錯誤詳情: {str(e)[:50]}")
        raise e
