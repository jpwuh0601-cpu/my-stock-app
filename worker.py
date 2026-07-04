import os
import yfinance as yf
import requests
import twstock
import pandas as pd
import traceback

def get_籌碼數據(ticker_symbol):
    """抓取法人買賣超資訊並轉換為 Markdown 表格"""
    try:
        code = ticker_symbol.split('.')[0]
        # 使用 twstock 抓取三大法人資料
        fetcher = twstock.ThreeInstitutionsFetcher()
        data = fetcher.fetch()
        
        # 轉換為 DataFrame 並過濾該股票
        df = pd.DataFrame(data)
        if 'stock_id' not in df.columns:
            return "無法獲取法人籌碼數據。"
            
        stock_data = df[df['stock_id'] == code].tail(10)
        
        if stock_data.empty:
            return "查無最近 10 日法人籌碼數據。"
            
        # 整理欄位顯示
        output_df = stock_data[['date', 'foreign_investor_buy_sell', 'investment_trust_buy_sell', 'dealer_buy_sell']]
        output_df.columns = ['日期', '外資', '投信', '自營商']
        
        return output_df.to_markdown(index=False)
    except Exception as e:
        return f"籌碼數據分析異常: {str(e)}"

def get_ai_analysis(ticker_symbol):
    """整合籌碼數據、新聞與 AI 深度分析的核心"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    ticker = yf.Ticker(ticker_symbol)
    
    try:
        # 1. 取得數據
        籌碼表 = get_籌碼數據(ticker_symbol)
        news_items = ticker.news
        latest_news = "\n".join([n.get('title', '') for n in news_items[:3]])
        
        # 2. 構建詳細 Prompt
        prompt = f"""
        請針對 {ticker_symbol} 進行深度金融分析。
        
        【三大法人 10 日買賣超明細】
        {籌碼表}
        
        【最近相關新聞】
        {latest_news}
        
        請完成以下任務並以 Markdown 格式輸出：
        1. 籌碼面解讀：分析法人買賣超趨勢與主力動向。
        2. 黑天鵝危機警示：評估風險等級 (安全/注意/危險) 並詳細說明警示原因。
        3. GPT 新聞解讀：綜合新聞觀點給予專業投資建議。
        """
        
        # 3. 呼叫 AI API
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "google/gemini-2.0-flash-exp:free", 
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=45)
        response_data = response.json()
        
        return response_data['choices'][0]['message']['content']
    
    except Exception as e:
        return f"AI 分析過程中發生錯誤: {str(e)}\n{traceback.format_exc()}"
