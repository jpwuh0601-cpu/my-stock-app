import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# 設定網頁標題
st.set_page_config(page_title="股市決策系統 (FinMind 台股版)", layout="wide")
st.title("📊 專業股市決策系統 (FinMind API)")

# 提示用戶 FinMind 使用說明
st.info("提示：FinMind 專為台股設計，請直接輸入代號 (例如: 2330, 2454)")

# 定義抓取資料函式 (使用 FinMind API)
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker, days=60):
    try:
        # FinMind API 獲取股價資料
        url = "https://api.finmindtrade.com/v2/api/data"
        params = {
            "dataset": "TaiwanStockPrice",
            "data_id": ticker,
            "start_date": (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        }
        response = requests.get(url, params=params, timeout=15)
        data = response.json()
        
        if data.get("status") == 200 and data.get("data"):
            df = pd.DataFrame(data["data"])
            # 標準化欄位名稱以符合後續邏輯
            df = df.rename(columns={"date": "Date", "open": "Open", "max": "High", "min": "Low", "close": "Close", "Trading_Volume": "Volume"})
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.set_index("Date").sort_index(ascending=False)
            return df[["Open", "High", "Low", "Close", "Volume"]]
        else:
            return "empty"
    except Exception as e:
        return str(e)

# 側邊欄
menu = st.sidebar.radio("功能選單", ["個股分析", "批量比較"])
# 新增日期範圍選擇器
days_filter = st.sidebar.slider("選擇資料顯示天數", 10, 180, 60)

if menu == "個股分析":
    ticker_input = st.text_input("輸入台股代號", "2330")
    if st.button("查詢分析"):
        with st.spinner(f"正在讀取近 {days_filter} 天的 FinMind 資料..."):
            result = fetch_stock_data(ticker_input.strip(), days=days_filter)
            if isinstance(result, pd.DataFrame):
                current_price = float(result['Close'].iloc[0])
                st.metric("最新收盤價", f"{round(current_price, 2)}")
                st.table(result.head(10)) # 顯示更多筆資料
            elif result == "empty":
                st.error("查無資料，請確認代號是否正確。")
            else:
                st.error(f"系統錯誤: {result}")

elif menu == "批量比較":
    st.subheader("⚖️ 股票數據批量比較")
    tickers_input = st.text_input("輸入代號 (逗號分隔)", "2330, 2454, 2317")
    if st.button("開始比較"):
        tickers = [t.strip() for t in tickers_input.split(",")]
        data = []
        success_count = 0
        
        with st.spinner("正在進行批量運算..."):
            for t in tickers:
                result = fetch_stock_data(t, days=days_filter)
                if isinstance(result, pd.DataFrame):
                    latest = float(result['Close'].iloc[0])
                    prev = float(result['Close'].iloc[1]) if len(result) > 1 else latest
                    change = ((latest - prev) / prev) * 100
                    data.append({
                        "代號": t, 
                        "最新價": round(latest, 2),
                        "漲跌幅 (%)": round(change, 2)
                    })
                    success_count += 1
                else:
                    data.append({"代號": t, "最新價": "查詢失敗", "漲跌幅 (%)": -999})
        
        if data:
            # 轉換為 DataFrame 並顯示，依照漲跌幅降冪排序
            df_comp = pd.DataFrame(data)
            df_comp = df_comp.sort_values(by="漲跌幅 (%)", ascending=False)
            
            # 定義顏色標記函式
            def highlight_change(val):
                if val == -999: return ""
                color = 'green' if val >= 0 else 'red'
                return f'color: {color}'
            
            # 使用自定義顯示格式：將失敗的 -999 顯示為 "-"
            def format_change(val):
                return f"{val:+.2f}%" if val != -999 else "-"
            
            # 應用樣式
            styled_df = df_comp.style.format({"漲跌幅 (%)": format_change}).applymap(highlight_change, subset=["漲跌幅 (%)"])
            
            st.dataframe(styled_df, use_container_width=True)
            
            # 新增視覺化長條圖
            valid_data = df_comp[df_comp["漲跌幅 (%)"] != -999]
            if not valid_data.empty:
                st.subheader("📈 漲跌幅視覺化比較")
                st.bar_chart(valid_data.set_index("代號")["漲跌幅 (%)"])
            
            st.success(f"比較完成！成功獲取 {success_count} 筆，失敗 {len(tickers) - success_count} 筆。")
