import json
import requests
import os
import yfinance as yf
import pandas as pd
import pandas_ta as ta
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

def get_ai_analysis(prompt, json_mode=False):
    """取得 AI 分析，並可選擇強制輸出 JSON"""
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"response_format": {"type": "json_object"}} if json_mode else {}
        )
        return completion.choices[0].message.content
    except Exception as e:
        return None

def fetch_news():
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

def calculate_technical_indicators(df):
    """計算 RSI, KD, MACD 指標"""
    # 計算 RSI
    df['RSI'] = ta.rsi(df['Close'], length=14)
    # 計算 KD (Stochastic Oscillator)
    stoch = ta.stoch(df['High'], df['Low'], df['Close'])
    # 計算 MACD
    macd = ta.macd(df['Close'])
    
    return {
        "RSI": round(df['RSI'].iloc[-1], 2),
        "KD": stoch.iloc[-1].to_dict() if stoch is not None else {},
        "MACD": macd.iloc[-1].to_dict() if macd is not None else {}
    }

def run_analysis_and_update():
    ticker = yf.Ticker("2330.TW")
    hist = ticker.history(period="6mo") # 取得較長數據以計算指標
    info = ticker.info
    
    # 1. 計算技術指標
    indicators = calculate_technical_indicators(hist)
    
    # 2. 強化財報預測 (強制輸出 JSON)
    report_prompt = "請分析台積電，並以 JSON 格式回傳: {'revenue': '金額', 'eps': '數值', 'dividend': '金額', 'summary': '分析內容'}"
    report_data = json.loads(get_ai_analysis(report_prompt, json_mode=True) or "{}")
    
    # 3. 新聞與黑天鵝分析
    news_list = fetch_news()
    black_swan_analysis = get_ai_analysis(f"根據新聞分析黑天鵝風險(JSON格式: {{'is_triggered': bool, 'reason': str}}): {news_list}", json_mode=True)
    black_swan_data = json.loads(black_swan_analysis or "{}")
    
    # 4. 選股邏輯 (加入技術指標作為參考)
    ai_selection = get_ai_analysis(f"當前技術指標為: {indicators}。基於此與市場氛圍，提供選股建議。")

    # 5. 組裝完整資料
    final_data = {
        "price": info.get("currentPrice", 0),
        "bvps": info.get("bookValue", 0),
        "financials": {"2025Q1": {"EPS": 5.2}},
        "institutional_investors": [],
        "news": news_list,
        "technical_indicators": indicators, # 傳入計算好的指標
        "est_revenue": report_data.get("revenue", "分析中"),
        "est_eps": report_data.get("eps", "分析中"),
        "est_dividend": report_data.get("dividend", "分析中"),
        "ai_prediction": report_data.get("summary", "分析中"),
        "margin_ratio": 0.0,
        "black_swan_alert": black_swan_data,
        "ai_stock_selection": ai_selection
    }
    
    save_market_data(final_data)
    send_line_notify(f"每日股市分析已更新: RSI={indicators['RSI']}")

if __name__ == "__main__":
    run_analysis_and_update()
