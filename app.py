import streamlit as st
import json
import pandas as pd
import plotly.express as px
import os

# 1. 設定頁面
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

# 2. 函式定義區 (必須放在最上方)
def load_data():
    file_path = "market_data.json"
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception as e:
        st.error(f"讀取資料錯誤: {e}")
        return {}

# 3. 主程式邏輯區
def main():
    st.title("📈 AI 智能金融監控終端")
    
    data = load_data()
    if not data:
        st.warning("數據載入中或檔案為空，請稍候...")
        return

    # 側邊欄：加入您想要的確定按鈕機制
    with st.sidebar.form(key='ticker_form'):
        selected_ticker = st.selectbox("請選擇股票代號", list(data.keys()))
        submit_button = st.form_submit_button(label='確定分析')

    # 當按下按鈕時才顯示數據
    if submit_button:
        ticker_data = data.get(selected_ticker, {})
        
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
    else:
        st.info("請從左側選擇股票後，點擊「確定分析」按鈕。")

if __name__ == "__main__":
    main()
