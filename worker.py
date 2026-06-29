import json
import requests
import os
import yfinance as yf
from datetime import datetime
from openai import OpenAI

# OpenRouter 設定
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def send_line_notify(message):
    token = os.getenv("LINE_NOTIFY_TOKEN")
    if not token: return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": message}
    try:
        requests.post(url, headers=headers, data=payload)
    except Exception as e:
        print(f"LINE 通知失敗: {e}")

def get_ai_analysis(prompt):
    """透過 OpenRouter 獲取 AI 分析"""
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini", # 可更換為其他 OpenRouter 模型
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI 分析暫時無法取得: {e}"

def save_market_data(data):
    data['update_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def run_analysis_and_update():
    # 1. 抓取真實數據
    ticker = yf.Ticker("2330.TW")
    info = ticker.info
    
    # 2. 呼叫 AI 進行財報預測與選股
    ai_prediction = get_ai_analysis("請根據台積電最新財報數據進行分析，並預估今年營收、EPS與股利。")
    ai_selection = get_ai_analysis("請根據當前台股市場氛圍，提供今日 AI 選股建議。")

    # 3. 組裝數據
    final_data = {
        "price": info.get("currentPrice", 0),
        "bvps": info.get("bookValue", 0),
        "financials": {"2025Q1": {"EPS": 5.2}},
        "institutional_investors": [],
        "news": ["最新市場動態..."],
        "technical_indicators": "強勢",
        "est_revenue": "AI 分析中...",
        "est_eps": "AI 分析中...",
        "est_dividend": "AI 分析中...",
        "ai_prediction": ai_prediction,
        "margin_ratio": 0.0,
        "black_swan_alert": {"is_triggered": False, "reason": "無"},
        "ai_stock_selection": ai_selection
    }
    
    save_market_data(final_data)
    send_line_notify(f"每日股市分析已更新: {final_data['ai_prediction'][:50]}...")

if __name__ == "__main__":
    run_analysis_and_update()
