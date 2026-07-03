import json
import logging
import yfinance as yf
import datetime
import time
import pandas as pd

# 設定日誌
logging.basicConfig(level=logging.INFO)

TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW"]
DATA_FILE = "market_data.json"

def run_analysis_and_update():
    logging.info("開始執行數據更新...")
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for symbol in TICKER_LIST:
        try:
            ticker = yf.Ticker(symbol)
            # 加入短暫延遲避免 429 Too Many Requests
            time.sleep(2) 
            
            info = ticker.info
            hist = ticker.history(period="1mo")
            
            # 強制轉換日期格式與數值型別
            hist_records = hist.reset_index()
            hist_records['Date'] = hist_records['Date'].dt.strftime('%Y-%m-%d')
            
            data[symbol] = {
                "price": float(ticker.fast_info.last_price),
                "eps": float(info.get("trailingEps", 0)),
                "bvps": float(info.get("bookValue", 0)),
                "pe": float(info.get("trailingPE", 0)),
                "history": hist_records.to_dict(orient='records'),
                "ai_prediction": "數據已自動更新。"
            }
            logging.info(f"股票 {symbol} 處理成功。")
        except Exception as e:
            logging.error(f"股票 {symbol} 處理失敗: {e}")
            
    # 安全寫入 JSON
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info("數據寫入完成。")
    except Exception as e:
        logging.error(f"寫入 JSON 失敗: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
