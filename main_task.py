import yfinance as yf
import json
import random

def get_stock_data(ticker):
    """
    獲取股票資訊並整合 8 項指定數據
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="10d")
    
    # 將歷史數據格式化為 JSON 友善格式
    institutional_data = []
    for date, row in hist.iterrows():
        institutional_data.append({
            "日期": date.strftime("%m-%d"),
            "外資": random.randint(-1000, 1000), # 模擬數據供測試
            "投信": random.randint(-500, 500),
            "自營商": random.randint(-300, 300)
        })
    
    # 整合 8 項數據結構
    data = {
        "price": info.get("currentPrice", 0),
        "change": info.get("regularMarketChange", 0),
        "nav": info.get("bookValue", 0),
        "pe": info.get("trailingPE", 0),
        "eps": info.get("trailingEps", 0),
        "quarterly_reports": "今年/去年Q1-Q4數據內容",
        "institutional_data": institutional_data,
        "broker_data": "十大主力券商數據內容",
        "ai_prediction": "AI財報預測分析內容",
        "revenue_forecast": "預估營收/EPS/股利數據",
        "news": "最新股市新聞快訊",
        "black_swan": "俄烏/美伊/聯準會警示內容",
        "tech_indicators": {"KD": 50, "MACD": 0, "RSI": 50},
        "shareholder_structure": {"1-10張": 40, "100-400張": 30, "1000張以上": 30}
    }
    return data

# 設定要監控的股票列表
tickers = ["2330.TW", "2317.TW", "2454.TW"]
full_data = {t: get_stock_data(t) for t in tickers}

# 寫入至 market_data.json
with open("market_data.json", "w", encoding="utf-8") as f:
    json.dump(full_data, f, ensure_ascii=False, indent=4)
