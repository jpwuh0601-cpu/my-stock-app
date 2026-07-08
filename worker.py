import yfinance as yf
import requests

def fetch_stock_data(ticker):
    """
    從 Yahoo Finance 抓取即時數據 (修正版)。
    採用偽裝瀏覽器 Header 與異常處理，確保連線穩定不卡死。
    """
    ticker = ticker.strip().upper()
    # 自動補齊台股代號格式
    if not ticker.endswith(".TW") and ticker.isdigit():
        ticker += ".TW"
    
    # 偽裝成瀏覽器請求，避免 Yahoo 伺服器因過頻請求而封鎖
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        # 建立 Session 並掛載 Header
        session = requests.Session()
        session.headers.update(headers)
        
        # 初始化 Ticker 物件
        stock = yf.Ticker(ticker, session=session)
        
        # 抓取基礎資訊 (info)
        info = stock.info
        
        # 優先嘗試取得即時股價，若 Yahoo API 沒回傳則由歷史紀錄補齊
        price = info.get("regularMarketPrice") or info.get("currentPrice") or 0
        if price == 0:
            hist = stock.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
        
        # 回傳結構化數據，確保各欄位有預設值，避免網頁崩潰
        return {
            "price": round(price, 2),
            "nav": info.get("bookValue", 0),
            "pe": round(info.get("trailingPE", 0), 2) if info.get("trailingPE") else 0,
            "eps": round(info.get("trailingEps", 0), 2) if info.get("trailingEps") else 0,
            "change": round(info.get("regularMarketChange", 0), 2) if info.get("regularMarketChange") else 0
        }
        
    except Exception as e:
        # 若發生錯誤，回傳結構化的錯誤訊息，讓前端顯示友好提示
        return {"error": f"連線失敗，請稍後再試: {str(e)}"}

if __name__ == "__main__":
    # 測試用：直接執行可驗證該代號是否能抓到資料
    print(fetch_stock_data("2330.TW"))
