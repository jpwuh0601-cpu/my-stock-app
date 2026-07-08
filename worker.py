import yfinance as yf
import requests

def normalize_ticker(ticker):
    """
    自動標準化代號：確保所有代號皆以 .TW 結尾
    """
    ticker = ticker.strip().upper()
    if not ticker.endswith(".TW") and ticker.isdigit():
        return ticker + ".TW"
    return ticker

def fetch_stock_data(ticker):
    """
    使用偽裝標頭抓取即時數據，確保穩定性
    """
    ticker = normalize_ticker(ticker)
    
    # 增加 User-Agent 偽裝，避免被 Yahoo Finance 伺服器阻擋
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # 使用 yfinance 的 session 功能來掛載 headers
        session = requests.Session()
        session.headers.update(headers)
        stock = yf.Ticker(ticker, session=session)
        
        # 獲取資訊與價格
        info = stock.info
        price = info.get("regularMarketPrice") or info.get("currentPrice") or 0
        
        # 若 price 為 0，可能是因為 Yahoo API 延遲，嘗試從 history 獲取
        if price == 0:
            hist = stock.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]

        return {
            "price": round(price, 2),
            "nav": info.get("bookValue", "N/A"),
            "pe": round(info.get("trailingPE", 0), 2) if info.get("trailingPE") else "N/A",
            "eps": round(info.get("trailingEps", 0), 2) if info.get("trailingEps") else "N/A",
            "change": round(info.get("regularMarketChange", 0), 2),
            "info": info
        }
    except Exception as e:
        return {"error": f"無法取得數據: {str(e)}"}

if __name__ == "__main__":
    # 測試用
    print(fetch_stock_data("2330.TW"))
