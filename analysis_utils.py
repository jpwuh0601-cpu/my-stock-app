import yfinance as yf

def get_stock_analysis(ticker):
    """共用的數據取得與計算邏輯"""
    df = yf.download(ticker, period="1mo", progress=False)
    if df.empty:
        return None, None, "數據取得失敗"
    
    # 確保轉換為 float 數值
    last_price = df['Close'].iloc[-1].item()
    sma_20 = df['Close'].rolling(window=20).mean().iloc[-1].item()
    
    # 判斷邏輯
    status = "多頭趨勢 (價格高於均線)" if last_price > sma_20 else "空頭趨勢 (價格低於均線)"
    
    return last_price, sma_20, status
