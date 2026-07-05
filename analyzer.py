import pandas as pd
import pandas_ta as ta
import yfinance as yf

def get_technical_indicators(ticker_symbol):
    """計算 RSI 與 KD 指標"""
    # 增加錯誤處理機制
    try:
        df = yf.download(ticker_symbol, period="1mo", interval="1d", progress=False)
        if df.empty or len(df) < 14:
            return "N/A", "N/A"
        
        # 確保資料為數值格式
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        
        rsi = ta.rsi(df['Close'], length=14)
        stoch = ta.stoch(df['High'], df['Low'], df['Close'])
        
        current_rsi = rsi.iloc[-1] if not rsi.empty else "N/A"
        current_k = stoch['STOCHk_14_3_3'].iloc[-1] if not stoch.empty else "N/A"
        
        return round(float(current_rsi), 2) if isinstance(current_rsi, float) else "N/A", \
               round(float(current_k), 2) if isinstance(current_k, float) else "N/A"
    except Exception as e:
        print(f"指標計算錯誤: {e}")
        return "N/A", "N/A"

def generate_ai_analysis(ticker_symbol, info):
    """生成結構化 AI 分析報告，包含觸發 LINE 通知用的關鍵字"""
    rsi, kd = get_technical_indicators(ticker_symbol)
    
    # 邏輯判斷：若 RSI 小於 40 且 K 值小於 30，AI 給予更積極的建議
    # 這有助於與 main_task.py 中的 "積極買入" 關鍵字對接
    advice = "觀望"
    if isinstance(rsi, float) and isinstance(kd, float):
        if rsi < 40 and kd < 30:
            advice = "積極買入"
        elif rsi > 70:
            advice = "建議減碼"
            
    prompt = f"""
    你是一位專業的證券分析師，請針對 {ticker_symbol} 進行綜合分析。
    
    【基本數據】：
    - 當前股價: {info.get('currentPrice', 'N/A')}
    - 本益比: {info.get('forwardPE', 'N/A')}
    
    【技術面指標】：
    - RSI (14): {rsi}
    - KD指標 (K值): {kd}
    
    請依照以下嚴謹格式分析：
    1. 【趨勢判斷】：綜合上述指標，判斷當前多空趨勢。
    2. 【投資建議】：明確給出「積極買入」、「觀望」或「建議減碼」。(系統分析建議為：{advice})
    3. 【核心理由】：簡短有力，指出關鍵技術支撐或壓力點。
    4. 【潛在風險】：指出一項目前最需關注的市場風險。
    """
    return prompt
