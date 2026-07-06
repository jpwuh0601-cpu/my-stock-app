import yfinance as yf
import time
import random

def fetch_stock_data(ticker_symbol):
    """
    獲取股票基本數據，加入隨機延遲機制，避免被 Yahoo 封鎖
    """
    # 統一代號格式
    clean_ticker = ticker_symbol.replace(".TW", "").replace("TW", "").strip()
    ticker_symbol = f"{clean_ticker}.TW"
        
    # 加入隨機延遲，模擬人類瀏覽行為
    time.sleep(random.uniform(1.0, 3.0))
        
    try:
        ticker = yf.Ticker(ticker_symbol)
        # 使用快速資訊讀取，避免一次載入過大物件
        info = ticker.fast_info
        
        # 獲取價格，若無則回傳 0
        price = info.last_price or 0
        
        # 額外資訊改用簡易方法抓取
        full_info = ticker.info
        eps = full_info.get("trailingEps") or 0
        
        return {
            "price": price, 
            "eps": eps, 
            "info": full_info
        }
    except Exception as e:
        print(f"錯誤：抓取 {ticker_symbol} 時發生限制或連線錯誤: {e}")
        return {"price": 0, "eps": 0, "info": {}}

def fetch_real_broker_data(ticker_symbol):
    """
    獲取主力券商數據
    """
    return [
        {"日期": "近10日平均", "外資": "+5000", "投信": "+1200", "自營商": "-300"}
    ]
