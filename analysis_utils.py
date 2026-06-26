# analysis_utils.py
import yfinance as yf

def get_stock_data(ticker):
    """共用的數據取得與處理函數"""
    df = yf.download(ticker, period="1mo", progress=False)
    if df.empty:
        return None, None, None
    
    sma_20 = df['Close'].rolling(window=20).mean().iloc[-1].item()
    last_price = df['Close'].iloc[-1].item()
    status = "多頭" if last_price > sma_20 else "空頭"
    
    return last_price, sma_20, status
