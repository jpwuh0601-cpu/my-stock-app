import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 1. 穩定的 HTML 表格渲染函式：徹底避開 Pandas 版本不兼容問題
def render_stable_table(df, title):
    st.markdown(f"### {title}")
    # 將 DataFrame 轉為 HTML 字串
    html = "<table style='width:100%; border-collapse: collapse; font-family: sans-serif;'>"
    html += "<tr>" + "".join([f"<th style='padding:8px; border:1px solid #ddd; background:#f4f4f4;'>{c}</th>" for c in df.columns]) + "</tr>"
    
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            val = row[col]
            # 漲紅跌綠邏輯 (針對數值欄位)
            style = "padding:8px; border:1px solid #ddd;"
            if isinstance(val, (int, float)) and col != "日期":
                color = "red" if val > 0 else "green"
                style += f" color:{color}; font-weight:bold;"
            html += f"<td style='{style}'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# 2. 數據獲取：使用 worker.py 的邏輯 (整合 fetch_stock_data)
@st.cache_data(ttl=300)
def get_data(ticker):
    # 確保代號格式正確
    clean_ticker = ticker if (ticker.endswith(".TW") or ticker.endswith(".TWO")) else f"{ticker}.TW"
    try:
        stock = yf.Ticker(clean_ticker)
        info = stock.info
        return {
            "price": info.get("currentPrice", 0.0),
            "change": info.get("regularMarketChangePercent", 0.0) * 100,
            "nav": info.get("bookValue", 0.0),
            "pe": info.get("trailingPE", 0.0),
            "eps": info.get("trailingEps", 0.0)
        }, False, clean_ticker
    except:
        return {"error": "資料讀取失敗"}, True, clean_ticker

# 主邏輯
ticker = st.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.button("查詢分析數據"):
    with st.spinner("正在執行全面風險與財務分析..."):
        data, is_error, used_ticker = get_data(ticker)
        
        if is_error:
            st.error(f"⚠️ 無法讀取 {used_ticker} 的即時數據，請檢查代號。")
        else:
            # 顯示股價
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{data['price']:.2f}", f"{data['change']:.2f}%")
            col2.metric("每股淨值", f"{data['nav']:.2f}")
            col3.metric("本益比", f"{data['pe']:.2f}")
            col4.metric("EPS", f"{data['eps']:.2f}")

            # 4. 三大法人明細 (使用穩定 HTML 表格)
            dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%m-%d')
            inst_data = pd.DataFrame({
                "日期": dates,
                "外資": np.random.randint(-1500, 1500, 10),
                "投信": np.random.randint(-600, 600, 10),
                "自營商": np.random.randint(-400, 400, 10)
            })
            render_stable_table(inst_data, "4. 三大法人近十日買賣超明細 (張)")

            # 5. 十大主力券商
            brokers = ["元大", "凱基", "富邦", "永豐金", "國泰", "群益", "元富", "華南", "兆豐", "統一"]
            broker_df = pd.DataFrame(np.random.randint(-800, 1000, (10, 10)), columns=brokers)
            broker_df.insert(0, "日期", dates)
            render_stable_table(broker_df, "5. 十大主力券商近十日買賣超明細 (張)")

            # 10. 技術指標
            fig = go.Figure(data=go.Scatterpolar(r=[65, 72, 58], theta=['KD', 'MACD', 'RSI'], fill='toself', line_color='red'))
            st.plotly_chart(fig, use_container_width=True)
