import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

# 設定網頁標題
st.set_page_config(page_title="股市決策系統 (FinMind 台股版)", layout="wide")
st.title("📊 專業股市決策系統 (FinMind API)")

st.info("提示：FinMind 專為台股設計，請直接輸入代號 (例如: 2330, 2454)")

@st.cache_data(ttl=3600)
def fetch_stock_data(ticker, days=60):
    try:
        url = "https://api.finmindtrade.com/v2/api/data"
        params = {
            "dataset": "TaiwanStockPrice",
            "data_id": ticker,
            "start_date": (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get("status") == 200 and data.get("data"):
            df = pd.DataFrame(data["data"])
            df = df.rename(columns={"date": "Date", "open": "Open", "max": "High", "min": "Low", "close": "Close", "Trading_Volume": "Volume"})
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.set_index("Date").sort_index(ascending=False)
            return df[["Open", "High", "Low", "Close", "Volume"]]
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
                st.error("查無資料或連線異常")

elif menu == "批量比較":
    st.subheader("⚖️ 股票數據批量比較")
    tickers_input = st.text_input("輸入代號 (逗號分隔)", "2330, 2454, 2317")
    if st.button("開始比較"):
        tickers = [t.strip() for t in tickers_input.split(",")]
        
        with st.spinner("正在併發處理批量運算..."):
            # 使用多執行緒同時查詢，解決轉圈卡死問題
            with ThreadPoolExecutor(max_workers=5) as executor:
                results = list(executor.map(lambda t: (t, fetch_stock_data(t, days=days_filter)), tickers))
            
            data = []
            success_count = 0
            for t, result in results:
                if isinstance(result, pd.DataFrame):
                    latest = float(result['Close'].iloc[0])
                    prev = float(result['Close'].iloc[1]) if len(result) > 1 else latest
                    change = ((latest - prev) / prev) * 100
                    data.append({"代號": t, "最新價": round(latest, 2), "漲跌幅 (%)": round(change, 2)})
                    success_count += 1
                else:
                    data.append({"代號": t, "最新價": "失敗", "漲跌幅 (%)": -999})
            
            if data:
                df_comp = pd.DataFrame(data).sort_values(by="漲跌幅 (%)", ascending=False)
                styled_df = df_comp.style.format({"漲跌幅 (%)": lambda x: f"{x:+.2f}%" if x != -999 else "-"})\
                                     .applymap(lambda x: 'color: green' if x >= 0 and x != -999 else ('color: red' if x < 0 else ''), subset=["漲跌幅 (%)"])
                st.dataframe(styled_df, use_container_width=True)
                
                valid_data = df_comp[df_comp["漲跌幅 (%)"] != -999]
                if not valid_data.empty:
                    st.bar_chart(valid_data.set_index("代號")["漲跌幅 (%)"])
                st.success(f"比較完成！成功 {success_count} 筆，失敗 {len(tickers) - success_count} 筆。")
