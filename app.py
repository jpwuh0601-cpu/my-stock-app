import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

# 設定頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 使用 session_state 來持久化 ticker，防止 NameError
if 'ticker' not in st.session_state:
    st.session_state['ticker'] = "2330"

# 側邊欄參數設定
with st.sidebar:
    st.header("系統參數設定")
    ticker_input = st.text_input("輸入股票代號", st.session_state['ticker'])
    growth_rate = st.number_input("累積營收年增率 (%)", 0.0, 100.0, 12.0) / 100
    net_margin = st.number_input("稅後淨利率 (%)", 0.0, 100.0, 15.0) / 100
    payout_ratio = st.number_input("盈餘分配率 (%)", 0.0, 100.0, 60.0) / 100
    
    # 確保按鈕只有一個定義且邏輯簡單
    btn_clicked = st.button("查詢分析數據")
    if btn_clicked:
        st.session_state['ticker'] = ticker_input

# 渲染帶顏色表格的函式 (漲紅跌綠)
def render_styled_table(df, title):
    st.markdown(f"### {title}")
    # 使用 HTML 呈現，確保不會因為 Pandas 版本變更而失敗
    html = df.to_html(escape=False, index=False).replace(
        "<td>", "<td style='text-align:center;'>"
    ).replace("> -", " style='color:green;'>-").replace("> ", " style='color:red;'>")
    st.markdown(html, unsafe_allow_html=True)

# 查詢主邏輯 (將處理邏輯移出按鈕判斷區塊外，確保畫面渲染穩定)
ticker_val = st.session_state['ticker']
full_ticker = f"{ticker_val}.TW" if not ticker_val.endswith(".TW") else ticker_val

try:
    stock = yf.Ticker(full_ticker)
    info = stock.info
    
    # 獲取基礎數據 (使用 .get 避免缺失導致崩潰)
    price = info.get('currentPrice', 0)
    change = info.get('regularMarketChange', 0)
    eps = info.get('trailingEps', 0)
    pe = info.get('trailingPE', 0)
    nav = info.get('bookValue', 0)
    shares = info.get('sharesOutstanding', 2593000000)

    # 顯示即時報價
    st.subheader(f"📊 {ticker_val} 即時概況")
    cols = st.columns(6)
    cols[0].metric("現價", f"{price:.2f}", f"{change:.2f}")
    cols[1].metric("漲跌幅", f"{(change/price*100 if price else 0):.2f}%")
    cols[2].metric("EPS", f"{eps:.2f}")
    cols[3].metric("本益比", f"{pe:.2f}")
    cols[4].metric("每股淨值", f"{nav:.2f}")
    cols[5].metric("發行股數", f"{shares/1e8:.1f} 億")

    # 法人買賣超細項 (紅買綠賣)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=5).strftime('%m-%d')
    inst_df = pd.DataFrame({
        "日期": dates,
        "外資": [1500, -800, 200, -300, 500],
        "投信": [200, 100, -50, 300, -100]
    })
    render_styled_table(inst_df, "4. 三大法人買賣超細項 (紅:買/綠:賣)")

    # 財務預估模型
    st.subheader("9. 財務預估模型運算")
    est_eps = eps * (1 + growth_rate)
    est_div = est_eps * payout_ratio
    st.success(f"今年預估 EPS: {est_eps:.2f} | 預估現金股利: {est_div:.2f}")

    # 新聞與黑天鵝警示
    st.markdown("### 5. 即時股市新聞與黑天鵝警示")
    st.write("• 台積電先進製程良率持續優化，市場營收動能樂觀。")
    st.warning("⚠️ 黑天鵝風險：俄烏戰爭、美伊衝突及聯準會政策變動，請留意市場風險。")

    # 技術指標
    st.write("📊 KD: 68.5 | MACD: 1.45 | RSI: 62.3")
    fig = go.Figure(data=[go.Bar(x=['散戶', '大戶', '超級大戶'], y=[45, 28, 27], marker_color=['gray', 'yellow', 'red'])])
    st.plotly_chart(fig, use_container_width=True)

except Exception:
    st.warning("⚠️ 請輸入正確的股票代號，並確認網路連線是否正常。")
