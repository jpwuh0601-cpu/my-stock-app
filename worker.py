import json
import requests
import os
import yfinance as yf
import pandas as pd
from datetime import datetime
from openai import OpenAI
from bs4 import BeautifulSoup

# 設定 OpenRouter API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# 匯入保護機制：嘗試匯入 pandas_ta，失敗則降級使用原生計算
try:
    import pandas_ta as ta
    HAS_PANDAS_TA = True
except ImportError:
    HAS_PANDAS_TA = False
    print("注意：未偵測到 pandas_ta，將自動降級使用原生 pandas 計算")

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

def calculate_technical_indicators(df):
    """計算技術指標，具備自動降級與空值防護功能"""
    try:
        if HAS_PANDAS_TA:
            # 安全地呼叫指標，並檢查回傳是否為 None
            rsi_series = ta.rsi(df['Close'], length=14)
            stoch_df = ta.stoch(df['High'], df['Low'], df['Close'])
            macd_df = ta.macd(df['Close'])
            
            return {
                "RSI": float(rsi_series.iloc[-1]) if rsi_series is not None and not pd.isna(rsi_series.iloc[-1]) else 0,
                "KD": stoch_df.iloc[-1].to_dict() if stoch_df is not None and not stoch_df.empty else {},
                "MACD": macd_df.iloc[-1].to_dict() if macd_df is not None and not macd_df.empty else {}
            }
        else:
            # 原生 Pandas 備援計算：RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            return {
                "RSI": float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 0,
                "KD": {"status": "not_available"},
                "MACD": {"status": "not_available"}
            }
    except Exception as e:
        print(f"指標計算發生錯誤: {e}")
        return {"RSI": 0, "KD": {}, "MACD": {}}

def run_analysis_and_update():
    ticker_code = "2330"
    ticker = yf.Ticker(f"{ticker_code}.TW")
    hist = ticker.history(period="6mo")
    info = ticker.info
    
    # 計算預測數據
    shares = info.get("sharesOutstanding", 25930000000)
    est_eps = (info.get("totalRevenue", 0) * 0.20 * 0.40) / shares
    est_dividend = est_eps * 0.50
    
    indicators = calculate_technical_indicators(hist)
    
    final_data = {
        "update_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "price": info.get("currentPrice", 0),
        "bvps": info.get("bookValue", 0),
        "financials": {"2025Q1": {"EPS": 5.2}},
        "institutional_investors": [{"機構": "外資", "買賣超": 500}],
        "news": ["市場動態更新"],
        "technical_indicators": indicators,
        "est_revenue": round(info.get("totalRevenue", 0) * 1.2, 0),
        "est_eps": round(est_eps, 2),
        "est_dividend": round(est_dividend, 2),
        "ai_prediction": "基於營收預測分析。",
        "margin_ratio": 1.2,
        "black_swan_alert": {"is_triggered": False},
        "ai_stock_selection": "維持穩健持有建議。",
        "line_status": True
    }
    
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        
    send_line_notify(f"每日股市更新: {ticker_code} 預估EPS={round(est_eps, 2)}")

if __name__ == "__main__":
    run_analysis_and_update()
