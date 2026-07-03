import json
import logging
import yfinance as yf
import datetime
import time
import os

# 設定日誌
logging.basicConfig(level=logging.INFO)

# 設定檔案路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "market_data.json")

# 【在此更新您的追蹤清單】
TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW", "1301.TW"]

def get_ticker_data(symbol):
    """取得個股數據，若失敗則返回初始值以避免程式中斷"""
    try:
        ticker = yf.Ticker(symbol)
        # 增加延遲避免被伺服器阻擋
        time.sleep(3) 
        info = ticker.info
        
        # 確保關鍵欄位存在
        return {
            "price": float(info.get("currentPrice") or info.get("regularMarketPrice") or 0.0),
            "eps": float(info.get("trailingEps") or 0.0),
            "pe": float(info.get("trailingPE") or 0.0),
            "ai_prediction": "數據已同步更新。"
        }
    except Exception as e:
        logging.error(f"取得 {symbol} 數據失敗: {e}")
        return {"price": 0.0, "eps": 0.0, "pe": 0.0, "ai_prediction": "數據獲取失敗"}

def run_analysis_and_update():
    """執行分析並將結果寫入 market_data.json"""
    logging.info(f"開始更新數據，寫入路徑: {DATA_FILE}")
    
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for symbol in TICKER_LIST:
        logging.info(f"正在處理: {symbol}")
        data[symbol] = get_ticker_data(symbol)
            
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info("market_data.json 寫入成功。")
    except Exception as e:
        logging.error(f"寫入檔案失敗: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
