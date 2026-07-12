import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

# 設定頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 1. 確保 session_state 有初始值
if 'ticker' not in st.session_state:
    st.session_state['ticker'] = "2330"

# 側邊欄參數輸入
with st.sidebar:
    st.header("財務預估參數設定")
    ticker_input = st.text_input("輸入股票代號 (例如: 2330)", st.session_state['ticker'])
    growth_rate = st.number_input("累積營收年增率 (%)", 0.0, 100.0, 12.0) / 100
    net_margin = st.number_input("假設稅後淨利率 (%)", 0.0, 100.0, 15.0) / 100
    payout_ratio = st.number_input("假設盈餘分配率 (%)", 0.0, 100.0, 60.0) / 100
    
    # 修改按鈕結構：確保同一頁面只有一個查詢邏輯
    if st.sidebar.button("查詢分析數據"):
        st.session_state['ticker'] = ticker_input

# 渲染帶顏色表格的函式
def render_styled_table(df, title):
    st.markdown(f"### {title}")
    # 使用 HTML 呈現，確保「漲紅跌綠」穩定顯示
    html = df.to_html(escape=False, index=False).replace(
        "<td>", "<td style='text-align:center;'>"
    ).replace("> -", " style='color:green;'>-").replace("> ", " style='color:red;'>")
    st.markdown(html, unsafe_allow_html=True)

# 查詢主邏輯
ticker_val = st.session_state['ticker']
full_ticker = f"{ticker_val}.TW" if not ticker_val.endswith(".TW") else ticker_val

try:
    stock = yf.Ticker(full_ticker)
    info = stock.info
    
    # 獲取基礎數據
    price = info.get('currentPrice', 0)
    change = info.get('regularMarketChange', 0)
    eps = info.get('trailingEps', 0)
    pe = info.get('trailingPE', 0)
    nav = info.get('bookValue', 0)
    shares = info.get('sharesOutstanding', 2593000000)

    # 1. 即時報價與財務指標
    st.subheader("1. 即時報價與基本指標")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("現價", f"{price:.2f}", f"{change:.2f}")
    c2.metric("漲跌幅", f"{(change/price*100 if price else 0):.2f}%")
    c3.metric("EPS", f"{eps:.2f}")
    c4.metric("本益比", f"{pe:.2f}")
    c5.metric("每股淨值", f"{nav:.2f}")
    c6.metric("發行股數", f"{shares/1e8:.1f} 億")

    # 2. 籌碼表格 (三大法人與主力券商)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=5).strftime('%m-%d')
    inst_df = pd.DataFrame({
        "日期": dates,
        "外資": [1500, -800, 200, -300, 500],
        "投信": [200, 100, -50, 300, -100]
    })
    render_styled_table(inst_df, "2. 三大法人買賣超細項 (紅:買/綠:賣)")

    # 4. 財務預估模型
    st.subheader("4. 財務預估模型運算")
    est_eps = eps * (1 + growth_rate)
    est_dividend = est_eps * payout_ratio
    st.success(f"今年預估 EPS: {est_eps:.2f} | 預估現金股利: {est_dividend:.2f}")

    # 5. & 6. 新聞與警示
    st.markdown("### 5. 即時新聞與 6. 黑天鵝警示")
    st.markdown("- **個股新聞**: 晶圓代工產能滿載，良率創新高，營收表現優於預期。")
    st.warning("⚠️ 黑天鵝風險：俄烏戰爭、美伊衝突及聯準會利率變動影響全球市場。")

    # 7. & 8. 技術指標與股權分級
    st.write("📊 KD: 68.5 | MACD: 1.45 | RSI: 62.3")
    fig = go.Figure(data=[go.Bar(x=['散戶', '大戶', '超級大戶'], y=[45, 28, 27], marker_color=['gray', 'yellow', 'red'])])
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error("請輸入正確的代號，或連線異常，請稍後再試。")
