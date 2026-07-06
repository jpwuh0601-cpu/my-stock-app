import streamlit as st
import pandas as pd
import json
import os
import yfinance as yf

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

# 側邊欄輸入
raw_ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
ticker = raw_ticker.strip().upper()

# 格式強制標準化：
# 1. 如果輸入純數字，補上 .TW
# 2. 如果輸入如 6456TW，修正為 6456.TW
if ticker.isdigit():
    ticker = f"{ticker}.TW"
elif ticker.endswith("TW") and not ticker.endswith(".TW"):
    ticker = ticker.replace("TW", ".TW")

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    
    # 邏輯 A：優先讀取 JSON 預分析資料
    if ticker in data_cache:
        st.success(f"已從離線資料庫載入 {ticker} 的深度分析")
        d = data_cache[ticker]
        st.metric("即時股價", f"{float(d.get('price', 0)):.2f}")
        st.subheader("法人籌碼分析")
        st.table(pd.DataFrame(d.get("institutional_data", [])))
        st.info(d.get("ai_prediction", "分析處理中..."))
    
    # 邏輯 B：即時補抓模式
    else:
        with st.spinner(f"正在嘗試即時獲取 {ticker} 的資訊..."):
            try:
                stock = yf.Ticker(ticker)
                # 使用 history 來確認該股票是否存在
                info = stock.info
                price = info.get("currentPrice") or info.get("regularMarketPrice")
                
                if price:
                    st.metric("即時股價 (即時抓取)", f"{float(price):.2f}")
                    st.info(f"系統提示：{ticker} 尚未列入每日自動分析清單，目前僅提供即時股價資訊。")
                else:
                    st.error(f"無法取得代號 {ticker} 的有效股價數據。請檢查該股票是否已下市或代號輸入錯誤。")
                    st.write(f"系統偵測代號為: {ticker}")
            except Exception as e:
                st.error(f"即時查詢發生錯誤: {str(e)}")

else:
    st.info("請輸入代號並點擊查詢。")
