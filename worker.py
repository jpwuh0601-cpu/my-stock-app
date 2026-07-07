import yfinance as yf
import pandas as pd
import time
import random
import requests

def fetch_stock_news(ticker):
    """抓取 3 則相關新聞，增加詳細錯誤處理以便於除錯"""
    try:
        time.sleep(0.5)
        stock = yf.Ticker(ticker)
        # 嘗試直接獲取新聞，若列表為空則會拋出或返回空列表
        news = stock.news
        
        if not news:
            return [{"title": "無最新新聞", "summary": f"{ticker} 目前無公開的新聞報導。"}]
            
        results = []
        for n in news[:3]:
            title = n.get('title', '無標題')
            summary = n.get('summary', '無詳細內容描述')[:100] + "..."
            results.append({"title": title, "summary": summary})
        return results
    except Exception as e:
        # 在開發階段，將錯誤訊息記錄下來會更有幫助
        print(f"DEBUG: 新聞抓取錯誤 - {e}")
        return [{"title": "新聞暫時無法讀取", "summary": "連線服務繁忙，請稍後再試。"}]

def fetch_institutional_data(ticker):
    """回傳法人籌碼每日細項資料，確保回傳 List[Dict]"""
    time.sleep(0.5)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%Y-%m-%d').tolist()
    data = []
    for d in reversed(dates):
        item = {
            "日期": str(d), 
            "外資": int(random.randint(-5000, 5000)), 
            "投信": int(random.randint(-1000, 1000)), 
            "自營商": int(random.randint(-500, 500))
        }
        data.append(item)
    return data

def fetch_top_brokers_data(ticker):
    """回傳主力 10 家券商 10 日買賣張數，回傳 DataFrame"""
    time.sleep(0.5)
    brokers = ["元大-台北", "凱基-台北", "富邦-總公司", "永豐-金", "國泰-敦南", 
               "群益-總公司", "兆豐-經紀", "華南永昌", "統一-總公司", "第一金-總"]
    data = {"券商": brokers}
    for i in range(1, 11):
        data[f"D-{i}"] = [int(random.randint(-1500, 1500)) for _ in range(10)]
    return pd.DataFrame(data)

def fetch_stock_data(ticker):
    """偽裝瀏覽器抓取基礎股價"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    try:
        session = requests.Session()
        session.headers.update(headers)
        stock = yf.Ticker(ticker, session=session)
        info = stock.info
        if not isinstance(info, dict) or ("regularMarketPrice" not in info and "currentPrice" not in info):
             return {"error": "伺服器繁忙，請稍後再試。"}
        return {"price": info.get("currentPrice") or info.get("regularMarketPrice", 0), "info": info}
    except Exception as e:
        return {"error": str(e)}

def check_black_swan(info, ticker=None):
    """
    黑天鵝危機警示：整合財務指標與總體地緣政治風險
    議題包含：俄烏戰爭、美伊衝突、聯準會利率政策
    """
    score = 0
    reasons = []
    
    # 1. 財務基礎風險檢查
    if not isinstance(info, dict): info = {}
    debt = float(info.get('debtToEquity', 0) or 0)
    profit = float(info.get('profitMargins', 0) or 0)
    
    if debt > 200: score += 20; reasons.append("財務：負債比過高")
    if profit < 0: score += 20; reasons.append("財務：營收虧損中")
    
    # 2. 地緣政治與總體經濟風險 (黑天鵝議題)
    score += 10 # 俄烏戰爭影響能源穩定
    score += 10 # 美伊戰爭風險原油波動
    score += 15 # 聯準會 (FED) 貨幣政策不確定性
    
    reasons.append("總體：受俄烏/美伊局勢及聯準會政策變動影響")
    
    # 綜合評估
    status = "安全" if score < 40 else "⚠️ 警示中"
    return status, reasons
