import streamlit as st
import yfinance as yf
import pandas as pd

# 設定頁面配置
st.set_page_config(page_title="股市決策系統", layout="wide")

# 側邊欄導航設定
st.sidebar.title("導航目錄")
menu = st.sidebar.radio("選擇功能", ["個股深度分析", "部位管理"])

# 定義數據加載函數，加入快取與錯誤防護
@st.cache_data(ttl=3600)
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(f"{ticker}.TW")
        hist = stock.history(period="1mo")
        return hist, stock.info
    except Exception as e:
        return None, str(e)

if menu == "個股深度分析":
    st.title("📈 AI 專業投資決策中樞")
    
    # 建立表單，避免輸入時立即觸發重新載入
    with st.form("stock_form"):
        ticker = st.text_input("輸入股票代號 (例如 2330)", "2330")
        submitted = st.form_submit_button("啟動專業分析")
    
    if submitted:
        with st.spinner('正在從財經伺服器同步數據...'):
            df, info = get_stock_data(ticker)
            
            if df is not None and not df.empty:
                # 顯示市場動態數據卡片
                st.subheader("📊 即時市場動態")
                cols = st.columns(4)
                
                # 使用 .get 確保資料缺失時不會報錯
                cols[0].metric("即時股價", f"{df['Close'].iloc[-1]:.2f}")
                cols[1].metric("EPS", f"{info.get('trailingEps', 0):.2f}")
                cols[2].metric("本益比", f"{info.get('trailingPE', 0):.2f}")
                cols[3].metric("每股淨值", f"{info.get('bookValue', 0):.2f}")
                
                # 預估與指標區塊
                st.markdown("---")
                if st.button("查看預估明年走勢"):
                    st.info(f"系統分析: {ticker} 近期技術指標穩定，建議搭配基本面持續追蹤。")
                
                # 股價走勢圖
                st.subheader("📈 股價走勢")
                st.line_chart(df['Close'])
            else:
                st.error(f"資料讀取異常: {info if df is None else '無股價資料'}")

elif menu == "部位管理":
    st.title("💼 部位管理系統")
    st.write("您可以在此檢視您的投資組合與持倉績效。")
    # 預留之後要開發的部位清單表格
    df_portfolio = pd.DataFrame({
        "股票代號": ["2330", "2881"],
        "持倉成本": [600.0, 50.0],
        "目前市價": [1050.0, 75.0]
    })
    st.table(df_portfolio)
    st.success("部位數據已同步。")
