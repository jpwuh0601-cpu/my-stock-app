import pandas as pd
import pandas_ta as ta
import yfinance as yf
from notifier import send_line_notify

def get_technical_indicators(ticker_symbol):
    """計算 RSI、KD 與移動平均線 (MA)"""
    try:
        # 下載更多歷史數據以計算 MA
        df = yf.download(ticker_symbol, period="3mo", interval="1d", progress=False)
        if df.empty or len(df) < 20:
            return "N/A", "N/A", "N/A"
        
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        
        # 指標計算
        rsi = ta.rsi(df['Close'], length=14)
        stoch = ta.stoch(df['High'], df['Low'], df['Close'])
        ma5 = ta.sma(df['Close'], length=5)
        ma20 = ta.sma(df['Close'], length=20)
        
        return round(float(rsi.iloc[-1]), 2), \
               round(float(stoch['STOCHk_14_3_3'].iloc[-1]), 2), \
               round(float(ma5.iloc[-1]), 2) > round(float(ma20.iloc[-1]), 2) # True 為黃金交叉
    except Exception as e:
        print(f"指標計算錯誤: {e}")
        return "N/A", "N/A", "N/A"

def generate_ai_analysis(ticker_symbol, info):
    """生成包含 MA 與減碼邏輯的實戰分析報告"""
    rsi, kd, is_golden_cross = get_technical_indicators(ticker_symbol)
    
    advice = "觀望"
    alert_msg = ""

    # 實戰決策邏輯
    if isinstance(rsi, (int, float)) and isinstance(kd, (int, float)):
        # 買入條件：RSI 低檔 + KD 低檔 + 黃金交叉
        if rsi < 40 and kd < 30 and is_golden_cross:
            advice = "積極買入"
            alert_msg = f"🚀 {ticker_symbol} 偵測到強力買進訊號！(均線黃金交叉)"
        
        # 風險控制：賣出/減碼條件
        elif rsi > 70 or (rsi > 60 and not is_golden_cross):
            advice = "建議減碼"
            alert_msg = f"⚠️ {ticker_symbol} 風險警示：超買或趨勢轉弱，建議減碼保護獲利。"

    # 若有觸發警示，發送通知
    if alert_msg:
        send_line_notify(alert_msg)
            
    return f"""
    【AI 實戰分析】{ticker_symbol}
    - 建議策略: {advice}
    - 技術指標: RSI {rsi}, KD {kd}
    - 均線狀態: {'黃金交叉 (多頭)' if is_golden_cross else '死亡交叉/整理 (空頭)'}
    - 綜合建議: 依照當前 {advice} 建議執行操作。
    """
