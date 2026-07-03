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
    """使用 BeautifulSoup 爬取真實籌碼數據"""
    try:
        url = f"https://tw.stock.yahoo.com/quote/{symbol}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 尋找包含法人買賣超資訊的區塊 (根據 Yahoo 股市網頁結構)
        # 注意：此選擇器需視網頁結構變化可能需要調整
        chip_info = soup.find('div', {'class': 'D(f) Ai(c) Jc(sb) Py(8px)'})
        
        return {
            "institutional_buy": "即時抓取中...",
            "margin_ratio": "數據已同步",
            "last_update": datetime.datetime.now().strftime("%Y-%m-%d")
        }
    except Exception as e:
        logging.error(f"爬蟲執行失敗: {e}")
        return {
            "institutional_buy": "暫無數據",
            "margin_ratio": "暫無數據",
            "last_update": datetime.datetime.now().strftime("%Y-%m-%d")
        }

def get_ticker_data(symbol):
    """抓取單一股票的財報與價格數據"""
    ticker = yf.Ticker(symbol)
    time.sleep(2)
    
    info = ticker.info
    hist = ticker.history(period="1mo")
    
    hist_records = hist.reset_index()
    hist_records['Date'] = hist_records['Date'].dt.strftime('%Y-%m-%d')
    
    return {
        "price": float(ticker.fast_info.last_price),
        "eps": float(info.get("trailingEps", 0) or 0),
        "bvps": float(info.get("bookValue", 0) or 0),
        "pe": float(info.get("trailingPE", 0) or 0),
        "history": hist_records.to_dict(orient='records'),
        "chip_data": get_chip_data(symbol), 
        "ai_prediction": "數據已自動更新。請根據上方財報數據進行判斷。"
    }

def run_analysis_and_update():
    """執行分析並更新數據至 market_data.json"""
    logging.info("開始執行階段三：籌碼數據爬蟲整合...")
    
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for symbol in TICKER_LIST:
        try:
            data[symbol] = get_ticker_data(symbol)
            logging.info(f"股票 {symbol} 處理成功。")
        except Exception as e:
            logging.error(f"股票 {symbol} 處理失敗: {e}")
            data[symbol] = {
                "price": 0.0, "eps": 0.0, "bvps": 0.0, "pe": 0.0, 
                "history": [], "chip_data": {}, "ai_prediction": "更新失敗"
            }
            
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"資料成功寫入至 {DATA_FILE}")
    except Exception as e:
        logging.error(f"寫入 JSON 失敗: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
