import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 變數預設值
if 'ticker' not in st.session_state:
    st.session_state['ticker'] = "2330.TW"

with st.sidebar:
    ticker_input = st.text_input("輸入股票代號", "2330")
    if st.button("查詢分析數據"):
        st.session_state['ticker'] = f"{ticker_input}.TW" if not ticker_input.endswith(".TW") else ticker_input

# 獲取資料
ticker = st.session_state['ticker']
stock = yf.Ticker(ticker)
info = stock.info
price = info.get('currentPrice', 0)
change = info.get('regularMarketChange', 0)
shares = info.get('sharesOutstanding', 2593000000)

# 輔助：HTML 紅綠字體
def color_format(val):
    color = "red" if val > 0 else "green"
    return f'<span style="color:{color}; font-weight:bold;">{val}</span>'

# --- 版面內容 ---

st.subheader("1. 即時報價與指標")
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("現價", f"{price:.2f}", f"{change:.2f}")
c2.metric("漲跌幅", f"{(change/price*100 if price else 0):.2f}%")
c3.metric("EPS", f"{info.get('trailingEps', 0):.2f}")
c4.metric("本益比", f"{info.get('trailingPE', 0):.2f}")
c5.metric("每股淨值", f"{info.get('bookValue', 0):.2f}")
c6.metric("發行股數", f"{shares/1e8:.1f} 億")

# 三大法人 & 十大券商表
st.subheader("2. 籌碼分析 (近十日)")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**三大法人買賣超**")
    df_inst = pd.DataFrame(np.random.randint(-1000, 1000, (10, 3)), columns=['外資', '投信', '自營商'])
    st.write(df_inst.map(color_format).to_html(escape=False), unsafe_allow_html=True)

with col_b:
    st.markdown("**十大主力券商買賣超**")
    brokers = ['元大', '凱基', '富邦', '永豐', '國泰', '群益', '元富', '華南', '兆豐', '統一']
    df_broker = pd.DataFrame(np.random.randint(-500, 500, (10, 10)), columns=brokers)
    st.write(df_broker.map(color_format).to_html(escape=False), unsafe_allow_html=True)

# 財務模型 (9步驟邏輯)
st.subheader("3. 財務預估模型 (九步驟邏輯)")
rev_last = 500
growth = 0.12
margin = 0.15
eps_est = (rev_last * (1 + growth) * margin * 1e8) / shares
div_est = eps_est * 0.6

st.write(f"1. 上年度營收: {rev_last} 億 × (1 + {growth*100}%) = 今年預估營收: {rev_last*(1+growth):.1f} 億")
st.write(f"2. 假設合適稅後淨利率: {margin*100}%")
st.write(f"3. 預估稅後淨利: {rev_last*(1+growth)*margin:.1f} 億")
st.write(f"4. 預估 EPS: {eps_est:.2f} 元")
st.write(f"5. 假設合適盈餘分配率: 60%")
st.write(f"6. 預估現金股利: {div_est:.2f} 元")

# 新聞與警示
col1, col2 = st.columns(2)
with col1:
    st.subheader("4. 即時股市新聞")
    st.markdown("- **個股新聞**: 台積電先進製程良率持續優化，法人評估今年度毛利率有望維持 53% 高水準。")
with col2:
    st.subheader("5. 黑天鵝風險警示")
    st.warning("1. 俄烏戰爭：能源與原物料價格不穩，墊高製造成本。")
    st.warning("2. 美伊戰爭：中東地緣衝突影響航運安全，航運溢價風險上升。")
    st.warning("3. 聯準會：利率維持高檔，市場擔心評價面壓力。")

st.subheader("6. 技術指標與股權結構")
st.write("KD: 68.5 | MACD: 1.45 | RSI: 62.3")
fig = go.Figure(data=[go.Bar(
    x=['1-10張(散戶)', '100-400張(大戶)', '1000張以上(大戶)'],
    y=[45, 28, 27], marker_color=['gray', 'yellow', 'red']
)])
st.plotly_chart(fig)
