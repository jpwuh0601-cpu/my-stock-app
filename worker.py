import yfinance as yf
import pandas as pd
import time
import random
import requests
import numpy as np
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_session():
    """建立帶有重試機制的 session，減少 Too Many Requests 錯誤"""
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    return session

def calculate_indicators(df):
    """計算技術指標，並處理空值"""
    if df.empty or len(df) < 26:
        return {"KD": "資料不足", "MACD": "資料不足", "RSI": "資料不足"}
    
    close = df['Close']
    
    # RSI 計算
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # KD 計算
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

def fetch_stock_data(ticker):
    """改良版資料抓取，增加 Session 與容錯機制"""
    try:
        session = get_session()
        stock = yf.Ticker(ticker, session=session)
        
        # 獲取基礎資訊，加入簡單重試
        info = stock.info
        if not info or not isinstance(info, dict):
            return {"error": "無法獲取股票資訊，請稍後重試。"}
            
        hist = stock.history(period="1mo")
        indicators = calculate_indicators(hist)
        
        # 確保價格欄位存在
        price = info.get("currentPrice") or info.get("regularMarketPrice") or 0
        
        result = {"price": price, "info": info}
        result.update(indicators)
        return result
    except Exception as e:
        return {"error": f"資料獲取異常: {str(e)}"}

def check_black_swan(info):
    """檢查財報風險，增加對 info 格式的嚴格檢查"""
    if not isinstance(info, dict):
        return "資料異常", ["無法解析財報資訊"]
    
    # 安全取得數值的 helper
    def get_val(key):
        try:
            return float(info.get(key, 0) or 0)
        except:
            return 0.0
            
    debt = get_val('debtToEquity')
    profit = get_val('profitMargins')
    
    score = 0
    reasons = []
    
    if debt > 200: score += 20; reasons.append("財務：負債比過高")
    if profit < 0: score += 20; reasons.append("財務：虧損中")
    
    # 風險因子
    score += 15; reasons.append("總體：國際局勢與聯準會政策風險")
    
    status = "安全" if score < 50 else "⚠️ 警示中"
    return status, reasons
