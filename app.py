import streamlit as st
import yfinance as yf
import pandas as pd

# 頁面配置：設定為寬螢幕模式以利資料展示
st.set_page_config(page_title="股市決策系統", layout="wide")

# 側邊欄導航選單
st.sidebar.title("導航目錄")
menu = st.sidebar.radio("選擇功能", ["個股深度分析", "部位管理"])

# 定義資料抓取函數：使用 @st.cache_data 進行快取，避免重複請求網路資源
@st.cache_data(ttl=3600)
def get_stock_data(ticker):
    """
    獲取個股基本資料與歷史走勢
    使用 standard yfinance 寫法，確保在各類環境下的兼容性
    """
    try:
        stock = yf.Ticker(f"{ticker}.TW")
        hist = stock.history(period="1mo")
        # 獲取基本面資料
        info = stock.info
        return hist, info
    except Exception as e:
        return None, str(e)

# 功能區塊一：個股深度分析
if menu == "個股深度分析":
    st.title("📈 AI 專業投資決策中樞")
    
    # 使用 st.form 結構：確保使用者點擊「啟動」後才觸發請求
    # 這是解決網頁剛打開就「轉圈圈」的關鍵
    with st.form("stock_form"):
        ticker = st.text_input("輸入股票代號 (例如 2330)", "2330")
        submitted = st.form_submit_button("啟動專業分析")
    
    if submitted:
        with st.spinner('正在從財經資料庫同步資訊...'):
            df, info = get_stock_data(ticker)
            
            if df is not None and not df.empty:
                st.subheader(f"📊 {ticker} 即時市場動態")
                cols = st.columns(4)
                
                # 顯示重點指標卡片，並處理潛在的資料缺失
                cols[0].metric("即時股價", f"{df['Close'].iloc[-1]:.2f}")
                cols[1].metric("EPS", f"{info.get('trailingEps', 0):.2f}")
                cols[2].metric("本益比", f"{info.get('trailingPE', 0):.2f}")
                cols[3].metric("每股淨值", f"{info.get('bookValue', 0):.2f}")
                
                # 繪製走勢圖
                st.markdown("---")
                st.subheader("📈 股價走勢")
                st.line_chart(df['Close'])
            else:
                st.error("無法取得該股資料，請確認代號是否正確。")

# 功能區塊二：部位管理
elif menu == "部位管理":
    st.title("💼 部位管理系統")
    st.write("您可以在此檢視您的投資組合與持倉績效。")
    
    # 範例部位資料
    portfolio_data = pd.DataFrame({
        "股票代號": ["2330", "2881"],
        "持倉成本": [600.0, 50.0],
        "目前市價": [1050.0, 75.0]
    })
    st.table(portfolio_data)
    st.success("部位數據已成功讀取。")
