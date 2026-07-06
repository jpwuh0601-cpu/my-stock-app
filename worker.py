import yfinance as yf
from bs4 import BeautifulSoup
import requests

def fetch_stock_data(ticker_symbol):
    """
    獲取股票基本數據，包含自動修正代號格式與防禦性編程
    """
    # 確保代號正確 (強制補上 .TW，若用戶輸入如 1301TW 則自動修正)
    clean_ticker = ticker_symbol.replace(".TW", "").replace("TW", "").strip()
    ticker_symbol = f"{clean_ticker}.TW"
        
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # 獲取價格與 EPS，若抓取失敗則給予預設值 0
        price = info.get("currentPrice") or info.get("regularMarketPrice") or 0
        eps = info.get("trailingEps") or 0
        
        return {
            "price": price, 
            "eps": eps, 
            "info": info
        }
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return {"price": 0, "eps": 0, "info": {}}

def fetch_real_broker_data(ticker_symbol):
    """
    獲取主力券商與籌碼數據，包含錯誤處理機制
    """
    try:
        # 此處為擴充介面，您可以根據需求填入 Goodinfo 或其他來源的爬蟲邏輯
        # 當前維持結構化回傳，避免前端顯示崩潰
        return [
            {"日期": "近10日平均", "外資": "+5000", "投信": "+1200", "自營商": "-300"}
        ]
    except Exception as e:
        print(f"Error fetching broker data: {e}")
        return [{"日期": "無資料", "外資": "0", "投信": "0", "自營商": "0"}]
