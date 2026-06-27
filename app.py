import streamlit as st
import yfinance as yf
import pandas as pd

# 設定網頁標題
st.set_page_config(page_title="專業股市 AI 決策系統", layout="wide")
st.title("📊 專業股市 AI 決策系統")

# 定義技術指標計算
def get_technical_indicators(df):
    if len(df) < 20:
        return df
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['MA20'] = df['Close'].rolling(window=20).mean()
    return df

@st.cache_data(ttl=3600)
def fetch_data(ticker):
    try:
        # 在雲端環境下，明確指定不使用過多的 session 快取，僅下載資料
        data = yf.Ticker(ticker)
        df = data.history(period="6mo")
        
        if df is None or df.empty:
            return None
            
        if 'Close' not in df.columns:
            return None
            
        df = get_technical_indicators(df)
        return df
    except Exception as e:
        st.error(f"資料獲取失敗: {str(e)}")
        return None

# 側邊欄導航與設定
menu = st.sidebar.radio("AI 決策核心", ["個股儀表板", "AI 選股與指標", "黑天鵝警示系統", "LINE 通知與 Bot 設定"])

if menu == "個股儀表板":
    ticker = st.text_input("輸入台股代號", "2330.TW")
    if st.button("查詢分析"):
        with st.spinner("獲取數據中..."):
            data = fetch_data(ticker)
            if data is not None and not data.empty:
                st.metric("最新收盤價", f"{round(data['Close'].iloc[-1], 2)}")
                st.line_chart(data[['Close', 'MA20']])
            else:
                st.error("無法獲取該代號資料。")

elif menu == "AI 選股與指標":
    st.subheader("🤖 AI 自動化選股系統")
    rsi_threshold = st.sidebar.slider("設定 RSI 超賣門檻", 20, 50, 30)
    
    if st.button("執行全市場掃描"):
        target_tickers = ["2330.TW", "2454.TW", "2317.TW", "3008.TW"]
        results = []
        with st.spinner(f"掃描中 (門檻: RSI < {rsi_threshold})..."):
            for t in target_tickers:
                df = fetch_data(t)
                if df is not None and 'RSI' in df.columns:
                    rsi_val = df['RSI'].iloc[-1]
                    if rsi_val < rsi_threshold:
                        results.append({"代號": t, "當前RSI": round(float(rsi_val), 2), "狀態": "超賣"})
        
        if results:
            df_results = pd.DataFrame(results)
            st.dataframe(df_results, use_container_width=True)
        else:
            st.info(f"目前無符合 RSI < {rsi_threshold} 的個股。")

elif menu == "黑天鵝警示系統":
    st.warning("⚠️ 黑天鵝監控中心")
    st.write("此模組可整合 LINE Notify 進行自動化提醒。")

elif menu == "LINE 通知與 Bot 設定":
    st.subheader("📱 LINE 服務整合設定")
    with st.expander("LINE Notify 設定"):
        st.write("用於接收黑天鵝警示推送。")
    with st.expander("LINE Messaging API 設定"):
        st.text_input("Channel Access Token", type="password")
        st.text_input("Webhook URL (公開連結)")
        if st.button("模擬測試 Webhook"):
            st.success("系統已準備好回應邏輯，請重新部署以完成生效。")
