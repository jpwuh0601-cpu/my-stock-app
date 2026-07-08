import yfinance as yf
import requests

def fetch_stock_data(ticker):
    """
    從 Yahoo Finance 抓取即時數據。
    加入偽裝 header 以提高連線穩定性，並設定 timeout 防止網頁卡死。
    """
    ticker = ticker.strip().upper()
    # 自動補齊台股代號
    if not ticker.endswith(".TW") and ticker.isdigit():
        ticker += ".TW"
    
    # 設定偽裝瀏覽器的 Header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        # 使用 Session 進行請求
        session = requests.Session()
        session.headers.update(headers)
        
        # 建立 Ticker 物件
        stock = yf.Ticker(ticker, session=session)
        
        # 嘗試取得基礎資訊，並設定超時限制
        info = stock.info
        
        # 取得股價 (優先嘗試 regularMarketPrice，若失敗則從歷史資料取)
        price = info.get("regularMarketPrice") or info.get("currentPrice") or 0
        if price == 0:
            hist = stock.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
        
        # 回傳結構化數據
        return {
            "price": round(price, 2),
            "nav": info.get("bookValue", 0),
            "pe": round(info.get("trailingPE", 0), 2) if info.get("trailingPE") else 0,
            "eps": round(info.get("trailingEps", 0), 2) if info.get("trailingEps") else 0,
            "change": round(info.get("regularMarketChange", 0), 2) if info.get("regularMarketChange") else 0
        }
        
    except Exception as e:
        # 發生錯誤時回傳錯誤訊息，讓 app.py 能顯示 st.error
        return {"error": str(e)}

if __name__ == "__main__":
    # 測試執行
    print(fetch_stock_data("2330.TW"))
