import json
import logging
import yfinance as yf
import datetime
import pandas as pd

# 設定日誌
logging.basicConfig(level=logging.INFO)

TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW"]
DATA_FILE = "market_data.json"

def run_analysis_and_update():
    """執行分析並更新數據"""
    logging.info("開始執行數據更新...")
    
    data = {
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    for symbol in TICKER_LIST:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1mo")
            
            # 將 DataFrame 轉為字典時，將日期轉為字串以防序列化失敗
            hist_records = hist.reset_index()
            hist_records['Date'] = hist_records['Date'].dt.strftime('%Y-%m-%d')
            
            data[symbol] = {
                "price": float(ticker.fast_info.last_price),
                "eps": info.get("trailingEps", "N/A"),
                "bvps": info.get("bookValue", "N/A"),
                "pe": info.get("trailingPE", "N/A"),
                "history": hist_records.to_dict(orient='records'),
                "ai_prediction": "數據已自動更新。"
            }
            logging.info(f"股票 {symbol} 處理成功。")
        except Exception as e:
            logging.error(f"股票 {symbol} 處理失敗: {e}")
    
    # 寫入 JSON
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logging.info("數據與時間戳記更新完成。")

if __name__ == "__main__":
    run_analysis_and_update()
