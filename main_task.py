import json
import os
import time
import yfinance as yf
from worker import fetch_stock_data, fetch_institutional_data
from analyzer import generate_ai_analysis

def get_tickers_from_file():
    """從 tickers.txt 讀取股票代號清單"""
    if os.path.exists("tickers.txt"):
        with open("tickers.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def run_main(target_tickers=None):
    """
    執行股市數據抓取與 AI 分析
    若未傳入 tickers，則自動讀取 tickers.txt
    """
    tickers = target_tickers if target_tickers else get_tickers_from_file()
    final_results = {}

    for ticker in tickers:
        print(f"🔍 正在更新: {ticker}")
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # 1. 取得股價歷史來補足資訊
        hist = stock.history(period="1d")
        last_price = float(hist['Close'].iloc[-1]) if not hist.empty else float(info.get('currentPrice', 0))
        
        # 2. 籌碼資料
        inst_data = fetch_institutional_data(ticker)
        
        # 3. 生成 AI 分析
        ai_res = generate_ai_analysis(ticker, str(info), str(inst_data))
        
        # 4. 修正欄位名稱，使其與 app.py 的需求完全對齊
        final_results[ticker] = {
            "price": last_price,
            "change": float(info.get("regularMarketChangePercent", 0)),
            "nav": float(info.get("bookValue", 0)),
            "pe": float(info.get("trailingPE", 0)),
            "eps": float(info.get("trailingEps", 0)),
            "margin_ratio": 0.0, 
            "institutional_data": inst_data if isinstance(inst_data, list) else [],
            "ai_prediction": ai_res.get("main_force_analysis", "分析中..."),
            "indicators": "RSI: 55, KD: 60"
        }
        time.sleep(5)

    # 寫入檔案
    output_path = os.path.join(os.getcwd(), "market_data.json")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(final_results, f, ensure_ascii=False, indent=4)
        print(f"✅ 資料已成功寫入，欄位已對齊: {output_path}")
    except Exception as e:
        print(f"❌ 寫入失敗: {e}")

if __name__ == "__main__":
    run_main()
