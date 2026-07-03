import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

# 設定頁面配置
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    file_path = "market_data.json"
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 確保讀取出來的確實是字典
            if isinstance(data, dict):
                return data
            return {}
    except Exception as e:
        st.error(f"讀取資料檔案發生錯誤: {e}")
        return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    
    data = load_data()
    
    # 檢查是否為空
    if not data:
        st.warning("目前沒有有效的市場數據，請等待自動化排程更新。")
        return

    # 選股選單
    tickers = list(data.keys())
    selected_ticker = st.sidebar.selectbox("請選擇股票代號", tickers)
    
    # 安全取得數據
    ticker_data = data.get(selected_ticker)
    
    if not isinstance(ticker_data, dict):
        st.error("該股票資料格式異常，請稍候。")
        return
    
    st.header(f"監控目標: {selected_ticker}")
    st.metric("即時股價", f"{float(ticker_data.get('price', 0)):,.2f}")
    
    st.divider()

    # 繪圖
    history = ticker_data.get("history", [])
    if history:
        df = pd.DataFrame(history)
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            fig = px.line(df, x="Date", y="Close", title=f"{selected_ticker} 走勢圖")
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("🤖 AI 智能分析")
    st.info(str(ticker_data.get("ai_prediction", "暫無分析數據")))

if __name__ == "__main__":
    main()
