import streamlit as st
import requests
import pandas as pd
import time
import random
from datetime import datetime, timedelta

# 設定網頁標題
st.set_page_config(page_title="股市決策系統 (FinMind 最終穩定版)", layout="wide")
st.title("📊 專業股市決策系統 (FinMind API)")

st.info("提示：已採取極致穩定模式，每次查詢間隔會自動拉長，避免連線失敗。")

def fetch_stock_data(ticker, days=60):
    try:
        # 強制執行序列間隔，這是確保雲端環境連線穩定的關鍵
        time.sleep(random.uniform(2.0, 3.0)) 
        
        url = "https://api.finmindtrade.com/v2/api/data"
        params = {
            "dataset": "TaiwanStockPrice",
            "data_id": ticker,
            "start_date": (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        }
        # 使用 timeout 確保單一請求不會阻塞主執行緒
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
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
                st.error("查無資料或連線逾時，請稍後再試。")

elif menu == "批量比較":
    st.subheader("⚖️ 股票數據批量比較")
    tickers_input = st.text_input("輸入代號 (逗號分隔)", "2330, 2454, 2317")
    if st.button("開始比較"):
        tickers = [t.strip() for t in tickers_input.split(",")]
        
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
            
            progress_bar.progress((i + 1) / len(tickers))
        
        if data:
            df_comp = pd.DataFrame(data).sort_values(by="漲跌幅 (%)", ascending=False)
            styled_df = df_comp.style.format({"漲跌幅 (%)": lambda x: f"{x:+.2f}%" if x != -999 else "-"})\
                                 .applymap(lambda x: 'color: green' if x >= 0 and x != -999 else ('color: red' if x < 0 else ''), subset=["漲跌幅 (%)"])
            st.dataframe(styled_df, use_container_width=True)
            st.success("比較完成！")
