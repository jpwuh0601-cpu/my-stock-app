import streamlit as st
import json
import os

st.set_page_config(page_title="AI 投資秘書儀表板", layout="wide")

st.title("📈 AI 投資秘書儀表板 (偵錯模式)")

# 偵錯：顯示目前目錄下有哪些檔案
st.write(f"目前工作目錄: {os.getcwd()}")
st.write(f"目錄下的檔案清單: {os.listdir('.')}")

def load_data():
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception as e:
            st.error(f"檔案存在但無法讀取: {e}")
            return None
    else:
        st.error(f"找不到檔案: {os.path.abspath(file_path)}")
        return None

data = load_data()

if data:
    st.success("成功載入數據！")
    tickers = list(data.keys())
    selected_ticker = st.sidebar.selectbox("請選擇分析個股", tickers)
    
    ticker_data = data.get(selected_ticker, {})
    st.header(f"個股分析: {selected_ticker}")
    st.write(ticker_data)
else:
    st.warning("請確保 GitHub Actions 完成後有成功產生 market_data.json 且已推送到 GitHub。")
