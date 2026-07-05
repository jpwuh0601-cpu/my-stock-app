import pandas as pd
import pandas_ta as ta
import yfinance as yf

def get_technical_indicators(ticker_symbol):
    """計算 RSI 與 KD 指標"""
    df = yf.download(ticker_symbol, period="1mo", interval="1d")
    if df.empty:
        return "N/A", "N/A"
    
    # 計算 RSI
    rsi = ta.rsi(df['Close'], length=14)
    # 計算 KD (Stochastic Oscillator)
    stoch = ta.stoch(df['High'], df['Low'], df['Close'])
    
    current_rsi = rsi.iloc[-1] if not rsi.empty else "N/A"
    current_k = stoch['STOCHk_14_3_3'].iloc[-1] if not stoch.empty else "N/A"
    
    return round(float(current_rsi), 2) if isinstance(current_rsi, float) else "N/A", \
           round(float(current_k), 2) if isinstance(current_k, float) else "N/A"

def generate_ai_analysis(ticker_symbol, info):
    """生成結構化 AI 分析報告"""
    rsi, kd = get_technical_indicators(ticker_symbol)
    
    prompt = f"""
    你是一位專業的證券分析師，請針對 {ticker_symbol} 進行綜合分析。
    
    【基本面數據】：
    - EPS: {info.get('trailingEps', 'N/A')}
    - 本益比 (PE): {info.get('forwardPE', 'N/A')}
    
    【技術面指標】：
    - RSI (14): {rsi}
    - KD指標 (K值): {kd}
    
    請依照以下嚴謹格式分析：
    1. 【趨勢判斷】：綜合基本面與技術面指標（特別是RSI與KD），判斷當前是超買、超賣或中性。
    2. 【投資建議】：明確給出「積極買入」、「觀望」或「建議減碼」。
    3. 【核心理由】：簡短有力，指出關鍵支撐或壓力點。
    4. 【潛在風險】：指出一項目前最需關注的市場風險。
    """
    return prompt
