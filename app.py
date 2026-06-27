import streamlit as st
import requests
import pandas as pd
import time
import random
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 設定網頁標題
st.set_page_config(page_title="股市決策系統 (FinMind 最終穩定版)", layout="wide")
st.title("📊 專業股市決策系統 (FinMind API)")

st.info("提示：已啟用防鎖死超時控制，若查詢逾時將直接顯示失敗，避免轉圈卡死。")

# 設定具有重試機制的 Session
@st.cache_resource
def get_session():
    session = requests.Session()
    # 減少重試次數，避免長時間等待
    retry = Retry(total=1, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    return session

def fetch_stock_data(ticker, days=60):
    try:
        session = get_session()
        # 強制停頓，這是繞過 API 頻率限制的必要手段
        time.sleep(random.uniform(1.5, 2.5)) 
        url = "https://api.finmindtrade.com/v2/api/data"
        params = {
            "dataset": "TaiwanStockPrice",
            "data_id": ticker,
            "start_date": (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        }
        # 強制縮短 Timeout，確保不卡死
        response = session.get(url, params=params, timeout=8)
        data = response.json()
        
        if data.get("status") == 200 and data.get("data"):
            df = pd.DataFrame(data["data"])
            df = df.rename(columns={"date": "Date", "open": "Open", "max": "High", "min": "Low", "close": "Close", "Trading_Volume": "Volume"})
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.set_index("Date").sort_index(ascending=False)
            return df[["Close"]]
        return "empty"
    except Exception:
        return "error"

menu = st.sidebar.radio("功能選單", ["個股分析", "批量比較"])
days_filter = st.sidebar.slider("選擇資料顯示天數", 10, 180, 60)

if menu == "個股分析":
    ticker_input = st.text_input("輸入台股代號", "2330")
    if st.button("查詢分析"):
        with st.spinner("正在讀取資料..."):
            result = fetch_stock_data(ticker_input.strip(), days=days_filter)
            if isinstance(result, pd.DataFrame):
                st.metric("最新收盤價", f"{round(float(result['Close'].iloc[0]), 2)}")
                st.table(result.head(10))
            else:
                st.error("查無資料或連線逾時")

elif menu == "批量比較":
    st.subheader("⚖️ 股票數據批量比較")
    tickers_input = st.text_input("輸入代號 (逗號分隔)", "2330, 2454, 2317")
    if st.button("開始比較"):
        tickers = [t.strip() for t in tickers_input.split(",")]
        
        # 加入進度條，提升 UI 反饋
        progress_bar = st.progress(0)
        data = []
        
        for i, t in enumerate(tickers):
            result = fetch_stock_data(t, days=days_filter)
            if isinstance(result, pd.DataFrame):
                latest = float(result['Close'].iloc[0])
                prev = float(result['Close'].iloc[1]) if len(result) > 1 else latest
                change = ((latest - prev) / prev) * 100
                data.append({"代號": t, "最新價": round(latest, 2), "漲跌幅 (%)": round(change, 2)})
            else:
                data.append({"代號": t, "最新價": "失敗", "漲跌幅 (%)": -999})
            
            # 更新進度條
            progress_bar.progress((i + 1) / len(tickers))
        
        if data:
            df_comp = pd.DataFrame(data).sort_values(by="漲跌幅 (%)", ascending=False)
            styled_df = df_comp.style.format({"漲跌幅 (%)": lambda x: f"{x:+.2f}%" if x != -999 else "-"})\
                                 .applymap(lambda x: 'color: green' if x >= 0 and x != -999 else ('color: red' if x < 0 else ''), subset=["漲跌幅 (%)"])
            st.dataframe(styled_df, use_container_width=True)
            st.success("比較完成！")
