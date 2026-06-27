# analysis_utils.py
import yfinance as yf
import time
import random

def get_stock_analysis(ticker):
    if not "." in ticker:
        ticker = f"{ticker}.TW"
    
    time.sleep(random.uniform(1, 2)) 
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    
    if hist.empty:
        return None, None, "數據取得失敗", {}
    
    # 技術數據
    last_price = hist['Close'].iloc[-1].item()
    prev_price = hist['Close'].iloc[-2].item()
    sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1].item()
    change_pct = ((last_price - prev_price) / prev_price) * 100
    status = "多頭" if last_price > sma_20 else "空頭"
    
    # 基本面數據 (若抓不到則補上 "N/A")
    info = stock.info
    data = {
        "現價": last_price,
        "漲跌幅": f"{change_pct:.2f}%",
        "EPS": info.get('trailingEps', 'N/A'),
        "本益比": info.get('trailingPE', 'N/A'),
        "每股淨值": info.get('bookValue', 'N/A'),
        "發行股數": info.get('sharesOutstanding', 'N/A')
    }
    
    return last_price, sma_20, status, data
