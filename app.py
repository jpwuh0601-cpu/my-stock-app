import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 使用 session_state 來持久化 ticker，防止 NameError
if 'ticker' not in st.session_state:
    st.session_state['ticker'] = "2330"

# 側邊欄：輸入區
with st.sidebar:
    st.header("參數設定")
    ticker_input = st.text_input("輸入股票代號", st.session_state['ticker'])
    growth_rate = st.number_input("累積營收年增率 (%)", 0.0, 100.0, 12.0) / 100
    net_margin = st.number_input("稅後淨利率 (%)", 0.0, 100.0, 15.0) / 100
    payout_ratio = st.number_input("盈餘分配率 (%)", 0.0, 100.0, 60.0) / 100
    
    if st.button("查詢分析數據"):
        st.session_state['ticker'] = ticker_input

# 資料處理邏輯
ticker_val = st.session_state['ticker']
full_ticker = f"{ticker_val}.TW" if not ticker_val.endswith(".TW") else ticker_val

try:
    stock = yf.Ticker(full_ticker)
    info = stock.info
    
    # 基本數據
    price = info.get('currentPrice', 0)
    change = info.get('regularMarketChange', 0)
    eps = info.get('trailingEps', 0)
    pe = info.get('trailingPE', 0)
    nav = info.get('bookValue', 0)
    shares = info.get('sharesOutstanding', 2593000000)

    # 顯示 1 & 2. 即時報價與指標
    st.subheader(f"📊 {ticker_val} 即時概況")
    cols = st.columns(6)
    cols[0].metric("現價", f"{price:.2f}", f"{change:.2f}")
    cols[1].metric("漲跌幅", f"{(change/price*100 if price else 0):.2f}%")
    cols[2].metric("EPS", f"{eps:.2f}")
    cols[3].metric("本益比", f"{pe:.2f}")
    cols[4].metric("每股淨值", f"{nav:.2f}")
    cols[5].metric("發行股數", f"{shares/1e8:.1f} 億")

    # 4 & 5. 法人與券商表格 (漲紅跌綠 HTML 渲染)
    def render_color_table(df, title):
        st.markdown(f"### {title}")
        html = df.to_html(escape=False, index=False).replace(
            "<td>", "<td style='text-align:center;'>"
        ).replace("> -", " style='color:green;'>-").replace("> ", " style='color:red;'>")
        st.markdown(html, unsafe_allow_html=True)

    # 模擬法人資料
    inst_data = pd.DataFrame({
        "日期": pd.date_range(end=pd.Timestamp.today(), periods=5).strftime('%m-%d'),
        "外資": [1500, -800, 200, -300, 500],
        "投信": [200, 100, -50, 300, -100]
    })
    render_color_table(inst_data, "4. 三大法人買賣超細項 (紅:買/綠:賣)")

    # 9. 財務預估模型
    st.subheader("9. 財務預估模型運算")
    est_eps = eps * (1 + growth_rate)
    est_div = est_eps * payout_ratio
    st.success(f"今年預估 EPS: {est_eps:.2f} | 預估現金股利: {est_div:.2f}")

except Exception as e:
    st.warning("⚠️ 請輸入正確的股票代號後，點擊查詢分析數據。")
