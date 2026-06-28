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

# 支援從環境變數讀取選股清單 (格式: "2330,2881,2603")，若無則使用預設值
WATCHLIST_ENV = os.getenv("WATCHLIST", "2330,2881,2603,2454")
WATCHLIST = WATCHLIST_ENV.split(",")

client = OpenAI(api_key=OPENAI_API_KEY)

def fetch_stock_data(ticker):
    try:
        logging.info(f"正在獲取股票數據: {ticker}")
        stock = twstock.Stock(ticker)
        data = stock.fetch_from(2026, 5) 
        df = pd.DataFrame(data)
        
        current_price = df['close'].iloc[-1]
        prev_price = df['close'].iloc[-2]
        change_pct = ((current_price - prev_price) / prev_price) * 100
        volume = df['capacity'].iloc[-1]
        ma5 = df['close'].rolling(window=5).mean().iloc[-1]
        
        trend = "📈 強勢" if current_price > ma5 else "📉 轉弱"
        
        # 風險檢查：跌幅超過 5% 加入警告標籤
        risk_alert = "🚨 風險提示: 跌幅異常" if change_pct <= -5 else ""
        
        return {
            "ticker": ticker, 
            "price": current_price, 
            "change": f"{change_pct:.2f}%", 
            "volume": int(volume), 
            "trend": trend,
            "risk_alert": risk_alert
        }
    except Exception as e:
        logging.error(f"獲取 {ticker} 數據失敗: {e}")
        return {"ticker": ticker, "price": 0, "trend": "數據錯誤", "risk_alert": ""}

def get_ai_insight(report_data):
    data_str = json.dumps(report_data, ensure_ascii=False)
    prompt = (f"以下是今日的股市監控數據: {data_str}。包含股價、漲跌幅、成交量及風險警示。請以專業投資顧問角度，"
              "分析這些股票的趨勢並給出具體操作建議。若有風險警示，請特別標註。請簡潔回覆，重點摘要，不超過 150 字。")
    
    try:
        logging.info("發送請求給 OpenAI 進行分析")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"AI 分析引擎失敗: {e}")
        return f"AI 分析服務暫時無法連線。"

def send_line_message(message_content):
    if not LINE_TOKEN:
        logging.error("未設定 LINE_CHANNEL_ACCESS_TOKEN")
        return
        
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}", "Content-Type": "application/json"}
    
    final_message = f"🤖 AI 深度決策報告\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{message_content}"
    payload = {"messages": [{"type": "text", "text": final_message}]}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        logging.info("LINE 通知發送成功")
    except Exception as e:
        logging.error(f"LINE 發送失敗: {e}")

if __name__ == "__main__":
    report_data = [fetch_stock_data(t) for t in WATCHLIST]
    ai_summary = get_ai_insight(report_data)
    
    msg = "【市場盤勢概覽】\n"
    for item in report_data:
        alert = f" {item['risk_alert']}" if item['risk_alert'] else ""
        msg += f"- {item['ticker']}: ${item['price']} (漲跌: {item.get('change', 'N/A')}, 量: {item.get('volume', 0)}){alert}\n"
    
    msg += f"\n【AI 深度觀點】\n{ai_summary}"
    send_line_message(msg)
