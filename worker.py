import yfinance as yf
import pandas as pd
import time
import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# (其他原有的函式保持不變...)

def check_black_swan(info):
    """
    檢查黑天鵝警示，加入三大宏觀議題：
    1. 俄烏戰爭升溫/談判進度
    2. 美伊戰爭與中東局勢
    3. 聯準會 (Fed) 利率政策與鷹鴿立場
    """
    if not isinstance(info, dict):
        return "安全", ["無數據"]
    
    reasons = []
    
    # 宏觀議題偵測 (模擬邏輯，實際應用可串接即時財經新聞 API)
    # 這裡我們可以加入一些針對當前日期 (2026-07-07) 的風險權重
    
    # 1. 聯準會議題 (範例：預測接下來有無升息/降息循環)
    # 假設這是一個變數，未來可由新聞分析器動態傳入
    reasons.append("聯準會 (Fed) 利率決策：市場關注接下來的降息循環節奏")
    
    # 2. 地緣政治 (俄烏/美伊)
    reasons.append("俄烏戰爭與中東情勢：地緣政治風險仍高，影響能源價格穩定")
    
    # 綜合評估邏輯
    # 若債務比過高或風險議題過多，則觸發警示
    debt = float(info.get('debtToEquity', 0) or 0)
    
    if debt > 150:
        reasons.append("公司財務槓桿較高，在宏觀風險下較敏感")
        return "⚠️ 警示中", reasons
    
    return "安全", reasons

# (其餘原有程式碼...)
