import json
import logging
import yfinance as yf
import datetime

# 設定日誌
logging.basicConfig(level=logging.INFO)

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
    """執行分析並更新數據"""
    all_results = {
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    for ticker_symbol in TICKER_LIST:
        try:
            ticker = yf.Ticker(ticker_symbol)
            fin = get_financials(ticker)
            price = ticker.fast_info.last_price
            
            all_results[ticker_symbol] = {
                "price": float(price),
                "bvps": fin["bvps"],
                "pe": fin["pe"],
                "eps": fin["eps"],
                "history": ticker.history(period="1mo")['Close'].reset_index().to_dict(orient='records'),
                "ai_prediction": "數據已更新，請根據當前財報數據進行判斷。"
            }
        except Exception as e:
            logging.error(f"股票 {ticker_symbol} 處理失敗: {e}")
    
    # 寫入檔案
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)
    logging.info("數據更新完成。")

if __name__ == "__main__":
    run_analysis_and_update()
