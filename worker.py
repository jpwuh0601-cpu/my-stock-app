import json
import logging
import yfinance as yf
import datetime
import time
import requests
from bs4 import BeautifulSoup

# 設定日誌
logging.basicConfig(level=logging.INFO)

# 設定監控標的與儲存路徑
TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW"]
DATA_FILE = "market_data.json"

def get_chip_data(symbol):
    """模擬爬蟲：未來可擴充為實際的 BeautifulSoup 解析邏輯"""
    # 這裡目前返回結構化數據，確保儀表板能正常運作且不報錯
    return {
        "institutional_buy": "外資買超 12,345 張",
        "margin_ratio": "15.2%",
        "last_update": datetime.datetime.now().strftime("%Y-%m-%d")
    }

def get_ticker_data(symbol):
    """抓取單一股票的財報與價格數據"""
    ticker = yf.Ticker(symbol)
    # 加入延遲以避免 Yahoo Finance 觸發 429 Too Many Requests 錯誤
    time.sleep(2)
    
    info = ticker.info
    hist = ticker.history(period="1mo")
    
    # 將日期格式化為字串，解決 Timestamp 序列化問題
    hist_records = hist.reset_index()
    hist_records['Date'] = hist_records['Date'].dt.strftime('%Y-%m-%d')
    
    return {
        "price": float(ticker.fast_info.last_price),
        "eps": float(info.get("trailingEps", 0) or 0),
        "bvps": float(info.get("bookValue", 0) or 0),
        "pe": float(info.get("trailingPE", 0) or 0),
        "history": hist_records.to_dict(orient='records'),
        "chip_data": get_chip_data(symbol), # 新增籌碼數據
        "ai_prediction": "數據已自動更新。請根據上方財報數據進行判斷。"
    }

def run_analysis_and_update():
    """執行分析並更新數據至 market_data.json"""
    logging.info("開始執行階段二：籌碼數據整合與財報更新...")
    
    # 初始化資料結構，包含最後更新時間
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for symbol in TICKER_LIST:
        try:
            data[symbol] = get_ticker_data(symbol)
            logging.info(f"股票 {symbol} 處理成功。")
        except Exception as e:
            logging.error(f"股票 {symbol} 處理失敗: {e}")
            # 若失敗則寫入預設空值，避免 JSON 結構崩潰
            data[symbol] = {
                "price": 0.0, "eps": 0.0, "bvps": 0.0, "pe": 0.0, 
                "history": [], "chip_data": {}, "ai_prediction": "更新失敗"
            }
            
    # 將結果安全寫入 JSON 檔案
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"資料成功寫入至 {DATA_FILE}")
    except Exception as e:
        logging.error(f"寫入 JSON 失敗: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
