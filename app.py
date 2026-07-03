import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    if not data:
        st.warning("目前正在更新數據，請稍候...")
        return

    # 側邊欄選擇器
    tickers = list(data.keys())
    selected_ticker = st.sidebar.selectbox("請選擇要分析的股票代號", tickers)
    
    # 確保資料存在
    ticker_data = data.get(selected_ticker)
    if not isinstance(ticker_data, dict):
        st.error("該股票資料格式異常。")
        return
    
    st.header(f"監控目標: {selected_ticker}")
    
    # AI 分析內容
    ai_text = str(ticker_data.get("ai_prediction", "暫無分析"))
    if "賣出" in ai_text:
        st.markdown(f'<h1 style="color:red;">⚠️ 賣出警告: {selected_ticker}</h1>', unsafe_allow_html=True)
    else:
        st.metric("即時股價", f"{float(ticker_data.get('price', 0)):,.2f}")
    
    st.divider()

    # 繪圖
    history = ticker_data.get("history", [])
    if history:
        df = pd.DataFrame(history)
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            fig = px.line(df, x="Date", y="Close", title=f"{selected_ticker} 近期走勢")
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("🤖 AI 智能分析報告")
    st.info(ai_text)

if __name__ == "__main__":
    main()
