import os
import yfinance as yf
import requests
import twstock
import pandas as pd
import traceback

def get_ai_analysis(ticker_symbol):
    api_key = os.getenv("OPENROUTER_API_KEY")
    ticker = yf.Ticker(ticker_symbol)
    
    # 取得籌碼數據
    code = ticker_symbol.split('.')[0]
    data = twstock.ThreeInstitutionsFetcher().fetch()
    df = pd.DataFrame(data)
    stock_data = df[df['stock_id'] == code].tail(10)
    
    # 強制將表格區塊獨立出來
    table_md = stock_data[['date', 'foreign_investor_buy_sell', 'investment_trust_buy_sell', 'dealer_buy_sell']].to_markdown(index=False)
    
    prompt = f"""
    請針對 {ticker_symbol} 進行簡潔有力的金融分析。
    
    【法人籌碼數據】
    {table_md}
    
    請依照以下嚴格格式輸出：
    
    ### 深度解讀
    (請濃縮在 300 字以內，專注趨勢與主力動向)
    
    ### 黑天鵝警示
    (等級：安全/注意/危險)
    (簡述原因)
    
    ### 投資建議
    (綜合觀點)
    """
    
    # (API 呼叫與原邏輯相同，將 Prompt 替換為上述內容)
    # ... 省略 API 請求細節 ...
