import yfinance as yf
import requests

def fetch_stock_data(ticker):
    """
    修正版資料獲取函式：
    1. 自動識別並轉換代號格式 (.TW)
    2. 加入 Header 模擬瀏覽器請求，避免被 Yahoo 擋下
    3. 增加健壯的錯誤處理機制
    """
    # 確保代號標準化處理
    ticker = ticker.strip().upper()
    
    # 自動補全台股代號格式
    if not ticker.endswith(".TW") and not ticker.endswith(".TWO"):
        if ticker.isdigit():
            # 依據常見規則，簡單判斷若為數字開頭則加上 .TW
            ticker += ".TW"
    
    # 模擬真實瀏覽器的 User-Agent，防止被 Yahoo Finance 擋下
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # 使用 Session 持續連線，提高效率
        session = requests.Session()
        session.headers.update(headers)
        
        stock = yf.Ticker(ticker, session=session)
        
        # 獲取財報與行情資料
        # 注意：info 請求較耗時，若失敗會拋出異常
        info = stock.info
        
        # 檢查是否獲取到有效資料
        # 排除 info 為空或找不到報價的情況
        if not info or ("regularMarketPrice" not in info and "currentPrice" not in info):
            return {"error": f"無法找到代號 {ticker} 的即時數據，請確認代號是否正確。"}
            
        price = info.get("regularMarketPrice") or info.get("currentPrice") or 0
        
        # 回傳結構化的數據
        return {
            "price": round(float(price), 2),
            "nav": round(float(info.get("bookValue", 0)), 2),
            "pe": round(float(info.get("trailingPE", 0)), 2) if info.get("trailingPE") else 0,
            "eps": round(float(info.get("trailingEps", 0)), 2) if info.get("trailingEps") else 0,
            "change": round(float(info.get("regularMarketChange", 0)), 2) if info.get("regularMarketChange") else 0
        }
        
    except Exception as e:
        # 將錯誤訊息回傳給 UI 顯示，便於除錯
        return {"error": f"資料獲取失敗: {str(e)}"}

if __name__ == "__main__":
    # 測試用：直接執行此檔案可驗證連線是否正常
    print(fetch_stock_data("2330.TW"))
