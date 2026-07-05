import pandas as pd
import pandas_ta as ta
import yfinance as yf
# 從您根目錄下的 notifier.py 導入通知功能
from notifier import send_line_notify

def get_technical_indicators(ticker_symbol):
    """計算 RSI 與 KD 指標"""
    try:
        df = yf.download(ticker_symbol, period="1mo", interval="1d", progress=False)
        if df.empty or len(df) < 14:
            return "N/A", "N/A"
        
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        rsi = ta.rsi(df['Close'], length=14)
        stoch = ta.stoch(df['High'], df['Low'], df['Close'])
        
        return round(float(rsi.iloc[-1]), 2), round(float(stoch['STOCHk_14_3_3'].iloc[-1]), 2)
    except Exception as e:
        print(f"指標計算錯誤: {e}")
        return "N/A", "N/A"

def generate_ai_analysis(ticker_symbol, info):
    """生成結構化 AI 分析報告，並自動觸發 LINE 通知"""
    rsi, kd = get_technical_indicators(ticker_symbol)
    
    # 邏輯判斷：若 RSI < 40 且 KD < 30，AI 給予更積極的建議
    advice = "觀望"
    if isinstance(rsi, (int, float)) and isinstance(kd, (int, float)):
        if rsi < 40 and kd < 30:
            advice = "積極買入"
            # 當偵測到買入訊號時，自動透過 notifier 發送 LINE 通知
            notification_msg = f"🚀 {ticker_symbol} 買入訊號通知！\n目前股價: {info.get('currentPrice', 'N/A')}\n技術面: RSI {rsi}, KD {kd}"
            send_line_notify(notification_msg)
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
    
    【分析判斷】：
    - 系統建議: {advice}
    
    請簡述您的核心理由與潛在風險。
    """
    return prompt
