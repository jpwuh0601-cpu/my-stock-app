import streamlit as st
import yfinance as yf
import pandas as pd

# 頁面配置
st.set_page_config(page_title="股市決策系統", layout="wide")

# 側邊欄導航
st.sidebar.title("導航目錄")
menu = st.sidebar.radio("選擇功能", ["個股深度分析", "部位管理"])

# 獲取股價函數
@st.cache_data(ttl=3600)
def get_current_price(ticker):
    try:
        stock = yf.Ticker(f"{ticker}.TW")
        price = stock.history(period="1d")['Close'].iloc[-1]
        return price
    except:
        return None

if menu == "個股深度分析":
    st.title("📈 AI 專業投資決策中樞")
    with st.form("stock_form"):
        ticker = st.text_input("輸入股票代號", "2330")
        submitted = st.form_submit_button("啟動專業分析")
    
    if submitted:
        # (這裡保留原本的深度分析邏輯)
        st.info("請參考右側部位管理查看損益分析。")

elif menu == "部位管理":
    st.title("💼 即時損益監控")
    
    # 定義您的持倉資料 (代號, 成本, 股數)
    portfolio = pd.DataFrame({
        "股票代號": ["2330", "2881"],
        "成本價": [600.0, 50.0],
        "持有股數": [1000, 2000]
    })
    
    # 動態抓取市價並計算損益
    with st.spinner("正在計算最新損益..."):
        prices = [get_current_price(t) for t in portfolio["股票代號"]]
        portfolio["目前市價"] = prices
        portfolio["總市值"] = portfolio["目前市價"] * portfolio["持有股數"]
        portfolio["損益金額"] = (portfolio["目前市價"] - portfolio["成本價"]) * portfolio["持有股數"]
        portfolio["報酬率 (%)"] = ((portfolio["目前市價"] - portfolio["成本價"]) / portfolio["成本價"]) * 100
        
        # 顯示表格
        st.table(portfolio.style.format({
            "目前市價": "{:.2f}",
            "損益金額": "{:,.0f}",
            "報酬率 (%)": "{:.2f}%"
        }))
        
        # 總結績效
        total_profit = portfolio["損益金額"].sum()
        if total_profit >= 0:
            st.metric("總損益 (TWD)", f"{total_profit:,.0f}", delta=f"{total_profit:,.0f}")
        else:
            st.metric("總損益 (TWD)", f"{total_profit:,.0f}", delta=f"{total_profit:,.0f}", delta_color="inverse")
            
    st.success("損益數據已同步更新。")
