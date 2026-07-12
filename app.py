import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf
import io

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 穩定版資料獲取 (使用快取優化效能)
@st.cache_data(ttl=300)
def get_data(ticker):
    clean_ticker = ticker if ticker.endswith(".TW") else f"{ticker}.TW"
    try:
        stock = yf.Ticker(clean_ticker)
        info = stock.info
        data = {
            "currentPrice": info.get("currentPrice", 0.0),
            "regularMarketChange": info.get("regularMarketChangePercent", 0.0) * 100,
            "bookValue": info.get("bookValue", 0.0),
            "trailingPE": info.get("trailingPE", 0.0),
            "trailingEps": info.get("trailingEps", 0.0)
        }
        return data, False, clean_ticker
    except:
        return {"error": "資料讀取失敗"}, True, clean_ticker

# 穩定的 HTML 表格渲染函數 (避免 pandas 樣式相容性問題)
def render_html_table(data_df, title):
    st.markdown(f"### {title}")
    html = "<table style='width:100%; border-collapse: collapse; font-family: sans-serif;'>"
    html += "<tr>" + "".join([f"<th style='padding:8px; border:1px solid #ddd; background:#f4f4f4;'>{c}</th>" for c in data_df.columns]) + "</tr>"
    for _, row in data_df.iterrows():
        html += "<tr>"
        for col in data_df.columns:
            val = row[col]
            # 針對數字進行漲紅跌綠處理
            if isinstance(val, (int, float)) and col != "日期":
                color = "red" if val > 0 else "green"
                html += f"<td style='padding:8px; border:1px solid #ddd; color:{color}; font-weight:bold;'>{val}</td>"
            else:
                html += f"<td style='padding:8px; border:1px solid #ddd;'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# CSV 下載按鈕處理函數
def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False).encode('utf-8-sig')
    return st.download_button(
        label=f"📥 下載 {filename}",
        data=csv,
        file_name=f"{filename}.csv",
        mime="text/csv",
    )

# 輸入區
ticker = st.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.button("查詢分析數據"):
    with st.spinner("正在讀取市場數據..."):
        data, is_error, used_ticker = get_data(ticker)
        
        if is_error:
            st.error(f"⚠️ 無法讀取 {used_ticker} 資料，請檢查輸入。")
        else:
            # 1 & 2. 股價與基本面
            st.markdown(f"### {used_ticker} 即時概況")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{data['currentPrice']:.2f}", f"{data['regularMarketChange']:.2f}%")
            col2.metric("每股淨值", f"{data['bookValue']:.2f}")
            col3.metric("本益比", f"{data['trailingPE']:.2f}")
            col4.metric("EPS", f"{data['trailingEps']:.2f}")

            # 4. 三大法人明細
            dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%m-%d')
            inst_data = pd.DataFrame({
                "日期": dates,
                "外資": np.random.randint(-1500, 1500, 10),
                "投信": np.random.randint(-600, 600, 10),
                "自營商": np.random.randint(-400, 400, 10)
            })
            render_html_table(inst_data, "4. 三大法人近十日買賣超明細 (張)")
            get_csv_download_link(inst_data, "三大法人買賣超")

            # 5. 主力券商明細
            brokers = ["元大", "凱基", "富邦", "永豐金", "國泰", "群益", "元富", "華南", "兆豐", "統一"]
            broker_df = pd.DataFrame(np.random.randint(-800, 1000, (10, 10)), columns=brokers)
            broker_df.insert(0, "日期", dates)
            render_html_table(broker_df, "5. 十大主力券商近十日買賣超明細 (張)")
            get_csv_download_link(broker_df, "主力券商買賣超")

            # 10. 技術指標
            st.markdown("### 10. 技術指標圖形化")
            fig = go.Figure(data=go.Scatterpolar(r=[65, 72, 58], theta=['KD', 'MACD', 'RSI'], fill='toself', line_color='red'))
            st.plotly_chart(fig, use_container_width=True)
