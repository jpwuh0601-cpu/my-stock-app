import yfinance as yf
import time
import random

def get_stock_analysis(ticker):
    # 自動補齊台股後綴
    if not "." in ticker:
        ticker = f"{ticker}.TW"
    
    # 加入 1-3 秒的隨機延遲，防止過度頻繁請求被 Yahoo 封鎖
    time.sleep(random.uniform(1, 3)) 
    
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    
    if hist.empty:
        return None, None, "數據取得失敗", {"營收": "N/A", "淨利": "N/A", "EPS": "N/A", "現金股利": "N/A"}
    
    # 計算技術指標
    last_price = hist['Close'].iloc[-1].item()
    sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1].item()
    status = "多頭趨勢 (價格高於均線)" if last_price > sma_20 else "空頭趨勢 (價格低於均線)"
    
    # 財報指標
    info = stock.info
    financials = {
        "營收": "N/A",
        "淨利": "N/A",
        "EPS": info.get('trailingEps', 'N/A'),
        "現金股利": info.get('dividendRate', 'N/A')
    }
    
    return last_price, sma_20, status, financials
