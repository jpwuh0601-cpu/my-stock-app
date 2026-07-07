import json
import os
import time
import yfinance as yf
from worker import fetch_stock_data, fetch_institutional_data
from analyzer import generate_ai_analysis

def run_main():
    tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]
    final_results = {}

    for ticker in tickers:
        print(f"🔍 正在更新: {ticker}")
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # 1. 取得股價歷史來補足資訊 (確保 price 有值)
        hist = stock.history(period="1d")
        last_price = float(hist['Close'].iloc[-1]) if not hist.empty else float(info.get('currentPrice', 0))
        
        # 2. 籌碼資料
        inst_data = fetch_institutional_data(ticker)
        
        # 3. 生成 AI 分析
        ai_res = generate_ai_analysis(ticker, str(info), str(inst_data))
        
        # 4. 強制寫入結構，針對數值欄位確保為 float
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

    # 寫入檔案 (明確路徑與寫入處理)
    output_path = os.path.join(os.getcwd(), "market_data.json")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(final_results, f, ensure_ascii=False, indent=4)
        print(f"✅ 資料已成功寫入: {output_path}")
    except Exception as e:
        print(f"❌ 寫入失敗: {e}")

if __name__ == "__main__":
    run_main()
