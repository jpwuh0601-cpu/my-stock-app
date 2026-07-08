import yfinance as yf
import requests

def fetch_stock_data(ticker):
    """
    修正後的資料獲取函式：
    1. 自動標準化股票代號格式 (確保 .TW 結尾)
    2. 加入瀏覽器 Header 模擬請求，防止被 API 封鎖
    3. 加入防呆與錯誤處理機制
    """
    # 1. 代號標準化：確保代號符合 Yahoo Finance 規範
    ticker = ticker.strip().upper()
    if not ticker.endswith(".TW") and not ticker.endswith(".TWO"):
        if ticker.isdigit():
            # 簡單判斷若為數字代號則自動加上 .TW
            ticker += ".TW"
    
    # 2. 模擬真實瀏覽器的 User-Agent，避免 Yahoo 封鎖請求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # 使用 Session 管理請求，提高連線穩定度
        session = requests.Session()
        session.headers.update(headers)
        
        # 建立 Ticker 物件
        stock = yf.Ticker(ticker, session=session)
        
        # 獲取資訊 (info 可能會觸發網路請求)
        info = stock.info
        
        # 3. 檢查資料有效性
        # 如果無法取得報價資料，則拋出異常讓例外處理區塊補捉
        if not info or ("regularMarketPrice" not in info and "currentPrice" not in info):
            return {"error": f"無法找到代號 {ticker} 的數據，請檢查代號是否正確。"}
            
        # 提取資料並進行型別安全轉換
        price = info.get("regularMarketPrice") or info.get("currentPrice") or 0
        
        return {
            "price": round(float(price), 2),
            "nav": round(float(info.get("bookValue", 0)), 2),
            "pe": round(float(info.get("trailingPE", 0)), 2) if info.get("trailingPE") else 0,
            "eps": round(float(info.get("trailingEps", 0)), 2) if info.get("trailingEps") else 0,
            "change": round(float(info.get("regularMarketChange", 0)), 2) if info.get("regularMarketChange") else 0
        }
        
    except Exception as e:
        # 將錯誤回傳，讓前端可以顯示錯誤訊息，而不是讓網頁崩潰
        return {"error": f"資料獲取失敗: {str(e)}"}

if __name__ == "__main__":
    # 單元測試用：可直接執行此檔案驗證 API 連線狀態
    print(fetch_stock_data("2330.TW"))
