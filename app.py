import json
import logging
import yfinance as yf
import datetime
import os

# 設定日誌
logging.basicConfig(level=logging.INFO)

# 設定監控標的與儲存路徑
TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW"]
DATA_FILE = "market_data.json"

def get_financials(ticker):
    """抓取財報基本面數據"""
    try:
        info = ticker.info
        return {
            "bvps": info.get("bookValue", 0),
            "pe": info.get("trailingPE", 0),
            "eps": info.get("trailingEps", 0)
        }
    except Exception as e:
        logging.error(f"財報抓取失敗: {e}")
        return {"bvps": 0, "pe": 0, "eps": 0}

def run_analysis_and_update():
    """執行分析並更新數據至 market_data.json"""
    logging.info("開始執行數據更新...")
    
    # 初始化資料結構，寫入當前時間戳記供回測檢核使用
    all_results = {
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    for ticker_symbol in TICKER_LIST:
        try:
            ticker = yf.Ticker(ticker_symbol)
            fin = get_financials(ticker)
            
            # 使用 fast_info 獲取即時價格，速度更快且更穩定
            price = ticker.fast_info.last_price
            
            all_results[ticker_symbol] = {
                "price": float(price),
                "bvps": fin["bvps"],
                "pe": fin["pe"],
                "eps": fin["eps"],
                "history": ticker.history(period="1mo")['Close'].reset_index().to_dict(orient='records'),
                "ai_prediction": "數據已自動更新。請根據上方財報數據與股價趨勢進行判斷。"
            }
            logging.info(f"股票 {ticker_symbol} 處理成功。")
            
        except Exception as e:
            logging.error(f"股票 {ticker_symbol} 處理失敗: {e}")
    
    # 將結果寫入 JSON 檔案
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=4)
        logging.info(f"數據成功寫入至 {DATA_FILE}")
    except Exception as e:
        logging.error(f"寫入 JSON 失敗: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
