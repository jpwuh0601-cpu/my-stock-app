import os
import requests
import twstock
import pandas as pd
from datetime import datetime
from openai import OpenAI

# 安全性提醒：請勿在此處直接填入金鑰，這些值會透過環境變數從 GitHub Secrets 自動注入
LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

WATCHLIST = ["2330", "2881", "2603", "2454"] 
client = OpenAI(api_key=OPENAI_API_KEY)

def fetch_stock_data(ticker):
    try:
        stock = twstock.Stock(ticker)
        data = stock.fetch_from(2026, 1)
        df = pd.DataFrame(data)
        current_price = df['close'].iloc[-1]
        ma5 = df['close'].rolling(window=5).mean().iloc[-1]
        trend = "📈 強勢" if current_price > ma5 else "📉 轉弱"
        return {"ticker": ticker, "price": current_price, "trend": trend}
    except Exception as e:
        return {"ticker": ticker, "price": 0, "trend": "數據錯誤"}

def get_ai_insight(report_data):
    # 將資料轉換為字串讓 AI 讀取
    data_str = str(report_data)
    prompt = f"以下是今日的股市監控數據: {data_str}。請用專業投資顧問的角度，簡短總結市場趨勢並給出操作建議，不超過 100 字。"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 分析引擎暫時無法連線: {e}"

def send_line_message(message_content):
    if not LINE_TOKEN:
        print("錯誤：未讀取到 LINE_TOKEN")
        return
        
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}", "Content-Type": "application/json"}
    
    final_message = f"🤖 AI 投資決策中樞\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{message_content}"
    payload = {"messages": [{"type": "text", "text": final_message}]}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("訊息發送成功")
    else:
        print(f"發送失敗: {response.text}")

if __name__ == "__main__":
    report_data = [fetch_stock_data(t) for t in WATCHLIST]
    ai_summary = get_ai_insight(report_data)
    
    msg = "【市場盤勢概覽】\n"
    for item in report_data:
        msg += f"- {item['ticker']}: {item['price']} ({item['trend']})\n"
    
    msg += f"\n【AI 深度觀點】\n{ai_summary}"
    send_line_message(msg)
