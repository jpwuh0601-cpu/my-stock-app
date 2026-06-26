import yfinance as yf

def get_stock_analysis(ticker):
    # 自動補齊台股後綴
    if not "." in ticker:
        ticker = f"{ticker}.TW"
    
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    
    if hist.empty:
        return None, None, "數據取得失敗", {}

    # 技術面計算
    last_price = hist['Close'].iloc[-1].item()
    sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1].item()
    status = "多頭趨勢" if last_price > sma_20 else "空頭趨勢"
    
    # 財務面資料 (嘗試抓取，若無則顯示 N/A)
    info = stock.info
    financials = {
        "營收": "N/A", # Yahoo Finance 對台股的詳細財報數據支援度較低
        "淨利": "N/A",
        "EPS": info.get('trailingEps', 'N/A'),
        "現金股利": info.get('dividendRate', 'N/A')
    }
    
    return last_price, sma_20, status, financials
