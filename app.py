import streamlit as st
import pandas_datareader.data as web
from datetime import datetime, timedelta
import pandas as pd

# 設定網頁標題
st.set_page_config(page_title="股市決策系統 (Stooq 穩定版)", layout="wide")
st.title("📊 專業股市決策系統 (Stooq 穩定版)")

st.info("提示：已切換至 Stooq 資料源，此來源對台股連線更為穩定。")

# 使用 st.cache_data 來儲存資料，避免重複網路請求
@st.cache_data(ttl=3600)
def fetch_stock_data_stooq(ticker, days=60):
    try:
        # Stooq 的台股代號格式通常為 2330.TW
        # 將 .TW 轉為 stooq 支援的格式，有些需改為 .TW
        symbol = ticker
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 使用 Stooq 抓取資料
        df = web.DataReader(symbol, 'stooq', start=start_date, end=end_date)
        
        if not df.empty:
            df = df.rename(columns={"Close": "收盤價", "Open": "開盤價", "High": "最高價", "Low": "最低價", "Volume": "成交量"})
            return df.sort_index(ascending=False)
        return None
    except Exception as e:
        return None

menu = st.sidebar.radio("功能選單", ["個股分析", "批量比較"])

if menu == "個股分析":
    ticker_input = st.text_input("輸入台股代號 (需加 .TW)", "2330.TW")
    if st.button("查詢分析"):
        data = fetch_stock_data_stooq(ticker_input.strip())
        if data is not None and not data.empty:
            latest = float(data['收盤價'].iloc[0])
            st.metric("最新收盤價", f"{round(latest, 2)}")
            st.table(data.head(5))
        else:
            st.warning("⚠️ 無法獲取資料，請檢查代號是否正確 (例如 2330.TW)。")

elif menu == "批量比較":
    st.subheader("⚖️ 批量比較 (請輸入 .TW 代號)")
    tickers_input = st.text_input("輸入代號 (逗號分隔)", "2330.TW, 2454.TW")
    if st.button("開始比較"):
        tickers = [t.strip() for t in tickers_input.split(",")]
        data_list = []
        
        for t in tickers:
            res = fetch_stock_data_stooq(t)
            if res is not None and not res.empty:
                latest = float(res['收盤價'].iloc[0])
                data_list.append({"代號": t, "最新價": round(latest, 2)})
            else:
                data_list.append({"代號": t, "最新價": "獲取失敗"})
                
        if data_list:
            st.table(pd.DataFrame(data_list))
