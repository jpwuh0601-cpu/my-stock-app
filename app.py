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
                return json.load(f)
        except:
            return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    if not data:
        st.warning("目前沒有數據，請等待自動化腳本運行。")
        return

    # 1. 股票選擇器 (動態讀取 JSON Keys)
    tickers = list(data.keys())
    selected_ticker = st.sidebar.selectbox("選擇股票代號", tickers)
    
    ticker_data = data.get(selected_ticker, {})
    
    # 2. 顯示數據
    st.header(f"監控目標: {selected_ticker}")
    
    # 警示邏輯
    ai_text = str(ticker_data.get("ai_prediction", ""))
    if "賣出" in ai_text:
        st.markdown(f'<h1 style="color:red;">⚠️ 賣出警告: {selected_ticker}</h1>', unsafe_allow_html=True)
    else:
        st.metric("即時股價", f"{float(ticker_data.get('price', 0)):,.2f}")
    
    st.divider()

    # 3. 歷史走勢圖
    history = ticker_data.get("history", [])
    if history:
        df_hist = pd.DataFrame(history)
        df_hist['Date'] = pd.to_datetime(df_hist['Date'])
        fig = px.line(df_hist, x="Date", y="Close", title=f"{selected_ticker} 近期股價趨勢")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🤖 AI 智能分析")
    st.write(ai_text)

if __name__ == "__main__":
    main()
