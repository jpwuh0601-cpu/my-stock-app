import json
import logging
import yfinance as yf
import datetime
import time

# 設定日誌
logging.basicConfig(level=logging.INFO)

TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW"]
DATA_FILE = "market_data.json"

def get_ticker_data(symbol):
    """抓取單一股票的財報與價格數據"""
    ticker = yf.Ticker(symbol)
    time.sleep(2) # 延遲請求以規避 429 錯誤
    
    info = ticker.info
    hist = ticker.history(period="1mo")
    hist_records = hist.reset_index()
    hist_records['Date'] = hist_records['Date'].dt.strftime('%Y-%m-%d')
    
    return {
        "price": float(ticker.fast_info.last_price),
        "eps": float(info.get("trailingEps", 0)),
        "bvps": float(info.get("bookValue", 0)),
        "pe": float(info.get("trailingPE", 0)),
        "history": hist_records.to_dict(orient='records'),
        "ai_prediction": "" # 預留空間給後續 AI 生成
    }

def run_analysis_and_update():
    logging.info("開始執行階段一：資料結構大補完...")
    
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for symbol in TICKER_LIST:
        try:
            data[symbol] = get_ticker_data(symbol)
            logging.info(f"股票 {symbol} 財報數據抓取成功。")
        except Exception as e:
            logging.error(f"股票 {symbol} 處理失敗: {e}")
            
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logging.info("資料更新完成，已準備好供前端渲染。")

if __name__ == "__main__":
    run_analysis_and_update()
