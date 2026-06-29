import json
import requests
import os
import yfinance as yf
import pandas as pd
from datetime import datetime
from openai import OpenAI
from bs4 import BeautifulSoup

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
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI 分析失敗: {e}"

def fetch_news():
    """抓取簡單的新聞標題"""
    try:
        url = "https://www.cnyes.com/news/cat/tw_stock"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        headlines = [h.text.strip() for h in soup.select('h3')[:5]]
        return headlines
    except:
        return ["無法取得最新新聞"]

def save_market_data(data):
    data['update_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def run_analysis_and_update():
    # 1. 真實台股資料抓取
    ticker = yf.Ticker("2330.TW")
    hist = ticker.history(period="1mo")
    info = ticker.info
    
    # 2. 新聞分析與黑天鵝警示邏輯
    news_list = fetch_news()
    news_summary = " ".join(news_list)
    black_swan_analysis = get_ai_analysis(f"根據這些新聞分析市場是否存在黑天鵝風險(回覆JSON格式: {{'is_triggered': bool, 'reason': str}}): {news_summary}")
    
    # 3. GPT AI 財報預測與選股
    ai_prediction = get_ai_analysis("分析台積電，預估今年營收、EPS與股利。")
    ai_selection = get_ai_analysis("基於當前市場氛圍，提供選股建議。")

    # 4. 組裝完整資料
    final_data = {
        "price": info.get("currentPrice", 0),
        "bvps": info.get("bookValue", 0),
        "financials": {"2025Q1": {"EPS": 5.2}},
        "institutional_investors": [],
        "news": news_list,
        "technical_indicators": f"近期收盤均價: {hist['Close'].mean():.2f}",
        "est_revenue": "AI 分析生成中...",
        "est_eps": "AI 分析生成中...",
        "est_dividend": "AI 分析生成中...",
        "ai_prediction": ai_prediction,
        "margin_ratio": 0.0,
        "black_swan_alert": json.loads(black_swan_analysis) if "{" in black_swan_analysis else {"is_triggered": False, "reason": "分析失敗"},
        "ai_stock_selection": ai_selection
    }
    
    save_market_data(final_data)
    send_line_notify(f"每日股市分析已更新: {ai_prediction[:30]}...")

if __name__ == "__main__":
    run_analysis_and_update()
