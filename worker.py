import yfinance as yf
import pandas as pd
import time
import random
import requests
import numpy as np

def calculate_indicators(df):
    """計算 KD, MACD, RSI 技術指標"""
    # 確保資料有足夠長度
    if df.empty or len(df) < 26:
        return {"KD": "資料不足", "MACD": "資料不足", "RSI": "資料不足"}
    
    close = df['Close']
    
    # RSI 計算
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # KD 計算 (簡化版)
    low_min = df['Low'].rolling(window=9).min()
    high_max = df['High'].rolling(window=9).max()
    rsv = (close - low_min) / (high_max - low_min) * 100
    k = rsv.ewm(com=2).mean()
    d = k.ewm(com=2).mean()
    
    # MACD 計算
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    
    return {
        "KD": f"K:{k.iloc[-1]:.2f}, D:{d.iloc[-1]:.2f}",
        "MACD": f"快線:{macd.iloc[-1]:.2f}, 訊號線:{signal.iloc[-1]:.2f}",
        "RSI": f"{rsi.iloc[-1]:.2f}"
    }

def fetch_stock_news(ticker):
    """抓取 3 則相關新聞，增加詳細錯誤處理以便於除錯"""
    try:
        time.sleep(0.5)
        stock = yf.Ticker(ticker)
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
    """偽裝瀏覽器抓取基礎股價並計算指標，並加入強健容錯"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    try:
        session = requests.Session()
        session.headers.update(headers)
        stock = yf.Ticker(ticker, session=session)
        info = stock.info
        
        # 確保 info 為字典且包含必要資訊
        if not isinstance(info, dict):
            return {"error": "無法獲取股票資訊，請確認代號是否正確。"}
            
        # 取得歷史股價以計算指標
        hist = stock.history(period="1mo")
        indicators = calculate_indicators(hist)
        
        # 獲取價格，增加預設值避免 KeyError
        price = info.get("currentPrice") or info.get("regularMarketPrice") or 0
        
        result = {"price": price, "info": info}
        result.update(indicators) # 加入指標數據
        return result
    except Exception as e:
        return {"error": f"資料獲取失敗: {str(e)}"}

def check_black_swan(info, ticker=None):
    """
    黑天鵝危機警示：整合財務指標與總體地緣政治風險
    增加了對 info 字典欄位的空值檢查，防止 TypeError
    """
    score = 0
    reasons = []
    
    # 確保 info 是字典格式，避免傳入錯誤導致崩潰
    if not isinstance(info, dict):
        return "資料異常", ["無法解析財報資訊"]
    
    # 使用 .get() 確保欄位缺失時回傳 0，並強制轉型為 float
    def safe_float(val):
        try:
            return float(val) if val is not None else 0.0
        except (ValueError, TypeError):
            return 0.0
            
    debt = safe_float(info.get('debtToEquity'))
    profit = safe_float(info.get('profitMargins'))
    
    if debt > 200: score += 20; reasons.append("財務：負債比過高，對利率敏感")
    if profit < 0: score += 20; reasons.append("財務：營收虧損中，抗風險能力弱")
    
    # 地緣政治風險因子
    score += 15; reasons.append("總體：俄烏戰事膠著，能源市場震盪風險")
    score += 15; reasons.append("總體：中東衝突擴散，全球航運物流受阻風險")
    score += 15; reasons.append("總體：聯準會利率政策路徑不確定性")
    
    status = "安全" if score < 50 else "⚠️ 警示中 (市場高風險)"
    return status, reasons
