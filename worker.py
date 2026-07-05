import yfinance as yf
import json
# 導入您新建的 analyzer 模組
from analyzer import generate_ai_analysis 

def get_ai_analysis_data(ticker_symbol):
    """
    獲取完整數據、計算指標並呼叫 analyzer 模組進行 AI 分析
    確保回傳的欄位結構符合 app.py 的讀取需求
    """
    stock = yf.Ticker(ticker_symbol)
    info = stock.info
    
    # 1. 取得 AI 分析觀點 (呼叫 analyzer.py 中的函式)
    analysis_prompt = generate_ai_analysis(ticker_symbol, info)
    
    # 2. 彙整數據，確保與 app.py 的欄位對接
    # app.py 預期有: price, eps, pe, black_swan, ai_prediction, news
    return {
        "price": info.get('currentPrice', info.get('regularMarketPrice', 0)),
        "eps": info.get('trailingEps', 0),
        "pe": info.get('forwardPE', 0),
        "black_swan": "安全" if info.get('trailingEps', 0) > 0 else "高風險", # 簡單的財務安全判斷邏輯
        "ai_prediction": analysis_prompt, 
        "news": "最新市場數據已整合技術分析指標。"
    }
