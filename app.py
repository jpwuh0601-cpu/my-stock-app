import streamlit as st
import json
import os
import yfinance as yf
import pandas as pd

# 設定頁面配置
st.set_page_config(page_title="即時投資決策儀表板", layout="wide")

st.title("📊 即時投資決策儀表板")

# 讀取數據的函式
def load_market_data():
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"讀取數據檔錯誤: {e}")
    return None

# 側邊欄查詢
st.sidebar.header("股票搜尋")
ticker_input = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")

if ticker_input:
    # 強制補上 .TW 確保 yfinance 可讀取
    ticker_symbol = f"{ticker_input}.TW"
    
    try:
        # 使用更穩定的 yfinance 呼叫方式，增加 session 處理
        ticker = yf.Ticker(ticker_symbol)
        # 嘗試取得當日數據，並加上 timeout 限制
        hist = ticker.history(period="1d", timeout=10)
        
        if hist.empty:
            st.error(f"無法取得 {ticker_symbol} 的資料，請確認代碼是否正確。")
        else:
            current_price = hist['Close'].iloc[-1]
            st.subheader(f"代碼: {ticker_input} 最新價格: {current_price:.2f}")
            
            # 嘗試讀取本地 JSON 數據作為補充資訊
            data = load_market_data()
            if data:
                st.write("---")
                st.write("### AI 智能分析")
                st.info(data.get("ai_prediction", "暫無分析數據"))
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("預估 EPS", data.get("est_eps", "N/A"))
                with col2:
                    st.metric("預估股利", data.get("est_dividend", "N/A"))
            else:
                st.warning("目前沒有 AI 分析數據可顯示。")
            
    except Exception as e:
        # 顯示詳細錯誤，方便排查網路連線問題
        st.error(f"系統發生錯誤: {str(e)}")
else:
    st.write("請在左側輸入台股代碼開始查詢。")

# 顯示最後更新時間
if os.path.exists("market_data.json"):
    st.sidebar.markdown(f"---")
    # 將時間戳轉為可讀格式
    last_mod = os.path.getmtime('market_data.json')
    st.sidebar.caption(f"數據最後更新於: {pd.to_datetime(last_mod, unit='s')}")
