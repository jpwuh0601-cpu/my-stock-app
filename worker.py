import yfinance as yf
import requests

def fetch_stock_data(ticker):
    """
    從 Yahoo Finance 抓取即時數據。
    採用偽裝瀏覽器 Header 與異常處理，確保連線穩定不卡死。
    """
    # 確保代號格式正確
    ticker = ticker.strip().upper()
    if not ticker.endswith(".TW") and ticker.isdigit():
        ticker += ".TW"
    
    # 偽裝成桌機瀏覽器請求，降低被 Yahoo 封鎖的機率
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        # 使用 Session 管理請求，提高連線穩定性
        session = requests.Session()
        session.headers.update(headers)
        
        # 建立 Ticker 物件
        stock = yf.Ticker(ticker, session=session)
        
        # 抓取基礎資訊 (info)
        info = stock.info
        
        # 優先嘗試取得即時股價，若 Yahoo API 沒回傳則由歷史紀錄補齊
        price = info.get("regularMarketPrice") or info.get("currentPrice") or 0
        if price == 0:
            hist = stock.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
        
        # 回傳結構化數據，確保各欄位有預設值，避免前端網頁崩潰
        return {
            "price": round(price, 2),
            "nav": info.get("bookValue", 0),
            "pe": round(info.get("trailingPE", 0), 2) if info.get("trailingPE") else 0,
            "eps": round(info.get("trailingEps", 0), 2) if info.get("trailingEps") else 0,
            "change": round(info.get("regularMarketChange", 0), 2) if info.get("regularMarketChange") else 0
        }
        
    except Exception as e:
        # 若發生錯誤，回傳結構化的錯誤訊息，讓 app.py 能顯示 st.error
        return {"error": f"連線失敗，請稍後再試: {str(e)}"}

if __name__ == "__main__":
    # 測試執行
    print(fetch_stock_data("2330.TW"))
