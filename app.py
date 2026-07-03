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
                # 確保載入的是字典
                return data if isinstance(data, dict) else {}
        except:
            return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    if not data:
        st.warning("目前沒有有效的數據，請稍候。")
        return

    # 顯示選單
    tickers = list(data.keys())
    selected_ticker = st.sidebar.selectbox("選擇股票代號", tickers)
    
    # 安全地取得數據
    ticker_data = data.get(selected_ticker)
    
    if ticker_data is None or not isinstance(ticker_data, dict):
        st.error(f"無法讀取 {selected_ticker} 的數據，格式可能異常。")
        return
    
    st.header(f"監控目標: {selected_ticker}")
    
    ai_text = str(ticker_data.get("ai_prediction", "無分析內容"))
    if "賣出" in ai_text:
        st.markdown(f'<h1 style="color:red;">⚠️ 賣出警告: {selected_ticker}</h1>', unsafe_allow_html=True)
    else:
        st.metric("即時股價", f"{float(ticker_data.get('price', 0)):,.2f}")
    
    st.divider()

    history = ticker_data.get("history", [])
    if history:
        df_hist = pd.DataFrame(history)
        if 'Date' in df_hist.columns:
            df_hist['Date'] = pd.to_datetime(df_hist['Date'])
            fig = px.line(df_hist, x="Date", y="Close", title=f"{selected_ticker} 走勢")
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("🤖 AI 智能分析")
    st.write(ai_text)

if __name__ == "__main__":
    main()
