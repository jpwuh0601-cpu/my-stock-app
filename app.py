import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

@st.cache_data(ttl=60)
def get_data(ticker):
    clean_ticker = ticker.strip()
    if not clean_ticker.endswith(".TW") and clean_ticker.isdigit():
        clean_ticker += ".TW"
        
    try:
        stock = yf.Ticker(clean_ticker)
        info = stock.info
        if not info or "currentPrice" not in info:
            return None, True, clean_ticker
            
        data = {
            "currentPrice": info.get("currentPrice", 0.0),
            "regularMarketChange": info.get("regularMarketChangePercent", 0.0) * 100,
            "bookValue": info.get("bookValue", 0.0),
            "trailingPE": info.get("trailingPE", 0.0),
            "trailingEps": info.get("trailingEps", 0.0)
        }
        return data, False, clean_ticker
    except Exception as e:
        return {"error": str(e)}, True, clean_ticker

# 確保在按鈕區塊外先定義 ticker
ticker_input = st.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.button("查詢分析數據"):
    # 使用正確的變數名稱 ticker_input
    with st.spinner("正在連線至市場資料庫..."):
        data, is_error, used_ticker = get_data(ticker_input)
        
        if is_error:
            st.error(f"⚠️ 無法取得 {used_ticker} 的資料。錯誤訊息: {data.get('error', '未知錯誤')}")
        else:
            st.success(f"成功取得 {used_ticker} 資料！")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{data['currentPrice']:.2f}", f"{data['regularMarketChange']:.2f}%")
            col2.metric("每股淨值", f"{data['bookValue']:.2f}")
            col3.metric("本益比", f"{data['trailingPE']:.2f}")
            col4.metric("EPS", f"{data['trailingEps']:.2f}")
            
            # 數據表格
            dates = pd.date_range(end=pd.Timestamp.today(), periods=5).strftime('%m-%d')
            inst_data = pd.DataFrame({"日期": dates, "外資": np.random.randint(-1000, 1000, 5)})
            st.markdown("### 4. 三大法人買賣超 (模擬)")
            st.dataframe(inst_data, use_container_width=True)
