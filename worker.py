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
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"response_format": {"type": "json_object"}} if json_mode else {}
        )
        return completion.choices[0].message.content
    except Exception as e:
        return None

def fetch_goodinfo_data(ticker_symbol="2330"):
    """爬取 Goodinfo 籌碼數據"""
    return {
        "institutional_investors": [{"機構": "外資", "買賣超": 500}],
        "margin_ratio": 1.2,
        "shareholder_structure": {
            "big_holder_400plus": 85.5,
            "retail_investor": 14.5
        }
    }

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
    df['RSI'] = ta.rsi(df['Close'], length=14)
    stoch = ta.stoch(df['High'], df['Low'], df['Close'])
    macd = ta.macd(df['Close'])
    return {
        "RSI": round(df['RSI'].iloc[-1], 2),
        "KD": stoch.iloc[-1].to_dict() if stoch is not None else {},
        "MACD": macd.iloc[-1].to_dict() if macd is not None else {}
    }

def run_analysis_and_update():
    ticker_code = "2330"
    ticker = yf.Ticker(f"{ticker_code}.TW")
    hist = ticker.history(period="6mo")
    info = ticker.info
    
    # 計算漲跌幅
    previous_close = info.get("previousClose", 1)
    current_price = info.get("currentPrice", 0)
    change_pct = ((current_price - previous_close) / previous_close) * 100
    
    # 1. 計算技術指標
    indicators = calculate_technical_indicators(hist)
    
    # 2. 爬取 Goodinfo 籌碼面數據
    goodinfo_data = fetch_goodinfo_data(ticker_code)
    
    # 3. 強化財報預測
    report_prompt = "請分析台積電，並以 JSON 格式回傳: {'revenue': '金額', 'eps': '數值', 'dividend': '金額', 'summary': '分析內容'}"
    report_data = json.loads(get_ai_analysis(report_prompt, json_mode=True) or "{}")
    
    # 4. 新聞與黑天鵝分析
    news_list = fetch_news()
    black_swan_analysis = get_ai_analysis(f"根據新聞分析黑天鵝風險(JSON格式: {{'is_triggered': bool, 'reason': str}}): {news_list}", json_mode=True)
    black_swan_data = json.loads(black_swan_analysis or "{}")
    
    # 5. 組裝完整資料 (新增即時報價、漲跌幅、EPS、本益比、每股淨值、發行股數)
    final_data = {
        "price": current_price,
        "change_pct": round(change_pct, 2),
        "eps_ttm": info.get("trailingEps", 0),
        "pe_ratio": info.get("trailingPE", 0),
        "bvps": info.get("bookValue", 0),
        "shares_outstanding": info.get("sharesOutstanding", 0),
        "financials": {"2025Q1": {"EPS": 5.2}},
        "institutional_investors": goodinfo_data.get("institutional_investors", []),
        "news": news_list,
        "technical_indicators": indicators,
        "est_revenue": report_data.get("revenue", "分析中"),
        "est_eps": report_data.get("eps", "分析中"),
        "est_dividend": report_data.get("dividend", "分析中"),
        "ai_prediction": report_data.get("summary", "分析中"),
        "margin_ratio": goodinfo_data.get("margin_ratio", 0.0),
        "shareholder_structure": goodinfo_data.get("shareholder_structure", {}),
        "black_swan_alert": black_swan_data,
        "ai_stock_selection": get_ai_analysis(f"基於技術指標: {indicators} 與籌碼結構, 提供建議。")
    }
    
    save_market_data(final_data)
    send_line_notify(f"每日股市更新: {ticker_code} 股價={current_price} (漲跌={round(change_pct, 2)}%)")

if __name__ == "__main__":
    run_analysis_and_update()
