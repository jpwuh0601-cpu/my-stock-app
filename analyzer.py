import pandas as pd
import pandas_ta as ta
import yfinance as yf
import streamlit as st
import requests

def send_line_notify(message):
    """從 analyzer 內直接調用的發送通知功能"""
    try:
        token = st.secrets.get("LINE_CHANNEL_ACCESS_TOKEN")
        if not token:
            return
        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {token}"}
        requests.post(url, headers=headers, data={"message": message})
    except Exception as e:
        print(f"通知發送失敗: {e}")

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
    except Exception:
        return "N/A", "N/A"

def generate_ai_analysis(ticker_symbol, info):
    """生成結構化 AI 分析報告"""
    rsi, kd = get_technical_indicators(ticker_symbol)
    advice = "觀望"
    if isinstance(rsi, float) and isinstance(kd, float):
        if rsi < 40 and kd < 30:
            advice = "積極買入"
            # 若為積極買入，直接觸發通知
            send_line_notify(f"🚀 {ticker_symbol} 偵測到積極買入訊號！")
        elif rsi > 70:
            advice = "建議減碼"
            
    return f"""
    【分析報告】{ticker_symbol}
    - 建議: {advice}
    - RSI: {rsi}, KD: {kd}
    """
