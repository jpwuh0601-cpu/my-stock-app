import os
import yfinance as yf
import requests
import twstock
import pandas as pd

def get_籌碼數據(ticker_symbol):
    """抓取法人買賣超資訊並轉換為 Markdown 表格"""
    try:
        code = ticker_symbol.split('.')[0]
        # 使用 twstock 抓取三大法人資料
        three_institutions = twstock.ThreeInstitutionsFetcher().fetch()
        df = pd.DataFrame(three_institutions)
        
        # 篩選該股票代號的資料，取最近 10 筆
        stock_data = df[df['stock_id'] == code].tail(10)
        
        # 轉換為 Markdown 表格
        return stock_data[['date', 'foreign_investor_buy_sell', 'investment_trust_buy_sell', 'dealer_buy_sell']].to_markdown(index=False)
    except Exception as e:
        return f"籌碼數據暫時無法讀取: {str(e)}"

def get_ai_analysis(ticker_symbol):
    """整合籌碼數據、新聞與 AI 深度分析的核心"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    ticker = yf.Ticker(ticker_symbol)
    
    # 1. 準備數據與新聞
    try:
        籌碼表 = get_籌碼數據(ticker_symbol)
        news = ticker.news
        latest_news = "\n".join([n['title'] for n in news[:3]])
        
        # 2. 構建深度分析 Prompt
        prompt = f"""
        請針對 {ticker_symbol} 進行深度金融分析。
        
        【三大法人 10 日買賣超明細】
        {籌碼表}
        
        【最近相關新聞】
        {latest_news}
        
        請完成以下任務並以 Markdown 格式輸出：
        1. 籌碼面解讀：分析法人買賣超趨勢。
        2. 黑天鵝危機警示：評估風險等級 (安全/注意/危險) 並說明原因。
        3. GPT 新聞解讀：綜合新聞觀點給予投資建議。
        """
        
        # 3. 呼叫 AI API
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "google/gemini-2.0-flash-exp:free", 
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
        return response.json()['choices'][0]['message']['content']
    
    except Exception as e:
        return f"深度分析暫時無法執行: {str(e)}"
