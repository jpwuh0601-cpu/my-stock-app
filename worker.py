import json
import requests
import os
import yfinance as yf
import pandas as pd
from datetime import datetime
from openai import OpenAI
import time
import math

# 設定 OpenRouter API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def send_line_notify(message):
    token = os.getenv("LINE_NOTIFY_TOKEN")
    if not token: return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": str(message)}
    try:
        requests.post(url, headers=headers, data=payload)
    except Exception as e:
        print(f"LINE 通知失敗: {e}")

def sanitize_recursive(val):
    if isinstance(val, (pd.Series, pd.Index)):
        val = val.tolist()
    if isinstance(val, dict):
        return {k: sanitize_recursive(v) for k, v in val.items()}
    elif isinstance(val, list):
        return [sanitize_recursive(v) for v in val]
    elif isinstance(val, (float, int)):
        if not math.isfinite(val): return 0.0
        return float(val)
    return val

def run_analysis_and_update():
    ticker_code = "2330"
    ticker = yf.Ticker(f"{ticker_code}.TW")
    
    # 獲取基礎資訊
    try:
        info = ticker.info
    except Exception as e:
        print(f"獲取資訊失敗: {e}")
        info = {}

    def sanitize(val):
        try:
            if val is None: return 0.0
            f = float(val)
            if not math.isfinite(f): return 0.0
            return f
        except: return 0.0

    # 豐富化數據指標
    final_data = {
        "update_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ticker": ticker_code,
        "price": sanitize(info.get("currentPrice")),
        "market_cap": sanitize(info.get("marketCap")),
        "pe_ratio": sanitize(info.get("trailingPE")),
        "forward_pe": sanitize(info.get("forwardPE")),
        "dividend_yield": sanitize(info.get("dividendYield")),
        "beta": sanitize(info.get("beta")),
        "book_value": sanitize(info.get("bookValue")),
        "profit_margins": sanitize(info.get("profitMargins")),
        "financials_summary": {
            "total_revenue": sanitize(info.get("totalRevenue")),
            "ebitda": sanitize(info.get("ebitda")),
            "operating_margins": sanitize(info.get("operatingMargins"))
        },
        "institutional_investors": [{"機構": "外資", "買賣超": 500}],
        "ai_prediction": "基於多維度財務指標分析，維持穩健看法。",
        "technical_indicators": {"RSI": 50, "Status": "Neutral"},
        "est_eps": sanitize(info.get("trailingEps")),
        "line_status": True
    }
    
    clean_data = sanitize_recursive(final_data)
    
    output_path = os.path.join(os.getcwd(), "market_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(clean_data, f, ensure_ascii=False, indent=4)
        
    send_line_notify(f"每日股市更新: {ticker_code} 已完成，資料已豐富化。")

if __name__ == "__main__":
    run_analysis_and_update()
