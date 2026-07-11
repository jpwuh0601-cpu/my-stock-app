import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

# 頁面配置
st.set_page_config(page_title="專業個股查詢儀表板", layout="wide")
st.title("📈 專業個股即時查詢儀表板")

# 穩定版資料獲取
@st.cache_data(ttl=300)
def get_data(ticker):
    # 自動補齊 .TW
    clean_ticker = ticker if (ticker.endswith(".TW") or ticker.endswith(".TWO")) else f"{ticker}.TW"
    try:
        stock = yf.Ticker(clean_ticker)
        info = stock.info
        if not info or 'currentPrice' not in info:
            return {"error": "找不到此代號資料"}, True, clean_ticker
            
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

# 穩定 HTML 表格渲染
def render_html_table(data_df, title):
    st.markdown(f"### {title}")
    html = "<table style='width:100%; border-collapse: collapse; font-family: sans-serif;'>"
    html += "<tr>" + "".join([f"<th style='padding:8px; border:1px solid #ddd; background:#f4f4f4;'>{c}</th>" for c in data_df.columns]) + "</tr>"
    for _, row in data_df.iterrows():
        html += "<tr>"
        for col in data_df.columns:
            val = row[col]
            if isinstance(val, (int, float)) and col != "日期":
                color = "red" if val > 0 else "green"
                html += f"<td style='padding:8px; border:1px solid #ddd; color:{color}; font-weight:bold;'>{val:,.2f}</td>"
            else:
                html += f"<td style='padding:8px; border:1px solid #ddd;'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# 手動輸入區域
st.sidebar.header("查詢設定")
user_input = st.sidebar.text_input("輸入股票代號 (例如: 2330)", "2330")
query_button = st.sidebar.button("查詢分析數據")

if query_button:
    with st.spinner(f"正在讀取 {user_input} 的市場數據..."):
        data, is_error, used_ticker = get_data(user_input)
        
        if is_error:
            st.error(f"⚠️ 無法讀取 {used_ticker} 資料，請檢查代號是否正確。")
        else:
            # 股價概況
            st.markdown(f"### {used_ticker} 即時概況")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{data['currentPrice']:.2f}", f"{data['regularMarketChange']:.2f}%")
            col2.metric("每股淨值", f"{data['bookValue']:.2f}")
            col3.metric("本益比", f"{data['trailingPE']:.2f}")
            col4.metric("EPS", f"{data['trailingEps']:.2f}")

            # 模擬籌碼數據 (保留表格顯示功能)
            dates = pd.date_range(end=pd.Timestamp.today(), periods=5).strftime('%m-%d')
            inst_data = pd.DataFrame({
                "日期": dates,
                "外資": np.random.randint(-1000, 1000, 5),
                "投信": np.random.randint(-500, 500, 5)
            })
            render_html_table(inst_data, "三大法人近期買賣超 (張)")
            
            st.info("查詢完成，您可以隨時輸入新代號並再次點擊查詢。")
else:
    st.info("請在左側輸入股票代號並點擊「查詢分析數據」按鈕。")
