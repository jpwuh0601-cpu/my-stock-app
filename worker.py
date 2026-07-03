import json
import logging
import yfinance as yf
import datetime
import time

# 設定日誌
logging.basicConfig(level=logging.INFO)

# 設定監控標的與儲存路徑
TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW"]
DATA_FILE = "market_data.json"

def get_ticker_data(symbol):
    """抓取並處理數據，確保可被 JSON 序列化"""
    ticker = yf.Ticker(symbol)
    # 增加延遲避免 Yahoo 封鎖
    time.sleep(3) 
    
    info = ticker.info
    hist = ticker.history(period="1mo")
    
    # 關鍵修正：將 Pandas 日期轉為原生字串
    hist_records = hist.reset_index()
    hist_records['Date'] = hist_records['Date'].dt.strftime('%Y-%m-%d')
    
    return {
        "price": float(ticker.fast_info.last_price or 0),
        "eps": float(info.get("trailingEps") or 0),
        "bvps": float(info.get("bookValue") or 0),
        "pe": float(info.get("trailingPE") or 0),
        "history": hist_records.to_dict(orient='records'),
        "ai_prediction": "數據已自動更新。"
    }

def run_analysis_and_update():
    logging.info("開始執行數據更新...")
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for symbol in TICKER_LIST:
        try:
            data[symbol] = get_ticker_data(symbol)
            logging.info(f"股票 {symbol} 處理成功。")
        except Exception as e:
            logging.error(f"股票 {symbol} 處理失敗: {e}")
            
    # 安全寫入 JSON
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logging.info("數據寫入完成。")

if __name__ == "__main__":
    run_analysis_and_update()
