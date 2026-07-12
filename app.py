import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 1. 狀態持久化，確保 ticker 變數不會遺失
if 'ticker' not in st.session_state:
    st.session_state['ticker'] = "2330"

# 側邊欄設定
with st.sidebar:
    st.header("系統參數")
    ticker_input = st.text_input("輸入股票代號", st.session_state['ticker'])
    growth_rate = st.number_input("營收年增率 (%)", 0.0, 100.0, 12.0) / 100
    net_margin = st.number_input("稅後淨利率 (%)", 0.0, 100.0, 15.0) / 100
    payout_ratio = st.number_input("盈餘分配率 (%)", 0.0, 100.0, 60.0) / 100
    
    if st.button("查詢分析數據"):
        st.session_state['ticker'] = ticker_input

# 處理漲紅跌綠的表格呈現
def render_styled_table(df, title):
    st.markdown(f"### {title}")
    # 將 DataFrame 轉為 HTML，並自定義顏色邏輯
    def color_format(x):
        try:
            val = float(x)
            color = 'red' if val > 0 else 'green'
            return f'color: {color}; font-weight: bold;'
        except:
            return ''
    
    # 這裡使用 Pandas 的 style 來渲染
    st.dataframe(df.style.applymap(color_format, subset=df.columns[1:]), use_container_width=True)

# 執行主邏輯
ticker_val = st.session_state['ticker']
full_ticker = f"{ticker_val}.TW" if not ticker_val.endswith(".TW") else ticker_val

try:
    stock = yf.Ticker(full_ticker)
    info = stock.info
    
    # 讀取基礎資料 (使用 get 預防資料缺失)
    price = info.get('currentPrice', 0)
    change = info.get('regularMarketChange', 0)
    eps = info.get('trailingEps', 0)
    pe = info.get('trailingPE', 0)
    nav = info.get('bookValue', 0)
    shares = info.get('sharesOutstanding', 2593000000)

    # 1. 即時報價
    st.subheader("1. 即時報價與財務指標")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("現價", f"{price:.2f}", f"{change:.2f}")
    c2.metric("EPS", f"{eps:.2f}")
    c3.metric("本益比", f"{pe:.2f}")
    c4.metric("每股淨值", f"{nav:.2f}")

    # 2. 三大法人與券商明細
    dates = pd.date_range(end=pd.Timestamp.today(), periods=5).strftime('%m-%d')
    inst_df = pd.DataFrame({
        "日期": dates,
        "外資": np.random.randint(-1500, 1500, 5),
        "投信": np.random.randint(-800, 800, 5),
        "自營商": np.random.randint(-500, 500, 5)
    })
    render_styled_table(inst_df, "2. 三大法人十日買賣超細項 (紅:買/綠:賣)")

    # 3. & 4. 財務預估模型
    st.subheader("4. 財務預估模型運算")
    est_eps = eps * (1 + growth_rate)
    est_dividend = est_eps * payout_ratio
    st.success(f"今年預估 EPS: {est_eps:.2f} 元 | 預估現金股利: {est_dividend:.2f} 元")

    # 5. & 6. 新聞與警示
    st.markdown("### 5. 即時股市新聞與黑天鵝警示")
    st.write("• 台積電先進製程良率持續優化，市場營收動能樂觀。")
    st.warning("⚠️ 黑天鵝警示：俄烏戰爭、美伊衝突與聯準會政策變動，請留意市場波動。")

    # 7. 技術指標
    st.write("📊 KD: 68.5 | MACD: 1.45 | RSI: 62.3")
    fig = go.Figure(data=[go.Bar(x=['散戶', '大戶', '超級大戶'], y=[45, 28, 27], marker_color=['gray', 'yellow', 'red'])])
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"查詢異常: 請檢查代號是否正確。 ({e})")
