import streamlit as st
from worker import fetch_stock_data, fetch_institutional_data

# 頁面配置
st.set_page_config(page_title="個股籌碼分析系統", layout="wide")

st.title("📈 個股籌碼分析系統")

# 使用快取函式，避免重複向 Yahoo 發送 API 請求
@st.cache_data(ttl=3600)
def get_data_cached(ticker):
    return fetch_stock_data(ticker)

# 側邊欄配置
st.sidebar.header("系統設定")
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在安全讀取資料中..."):
        data = get_data_cached(ticker)
        
        # 錯誤狀態判斷
        if isinstance(data, dict) and data.get("error"):
            st.error(f"系統訊息: {data['error']}")
        else:
            info = data.get("info", {})
            
            # 顯示基礎指標
            st.subheader("1. 股價與財務數據")
            c1, c2, c3 = st.columns(3)
            c1.metric("即時股價", f"{info.get('currentPrice', 0):.2f}")
            c2.metric("EPS", f"{data.get('eps', 0):.2f}")
            c3.metric("本益比", f"{info.get('forwardPE', 0):.2f}")
            
            # 顯示法人數據
            st.subheader("2. 法人籌碼統計")
            try:
                inst_df = fetch_institutional_data(ticker)
                st.table(inst_df.set_index("日期"))
            except:
                st.warning("目前無籌碼數據。")
            
            # 顯示新聞 (安全讀取)
            st.subheader("3. 最新新聞")
            news = info.get("news", [])
            if news:
                for n in news[:5]: # 只顯示前 5 則
                    if 'title' in n:
                        st.write(f"- {n['title']}")
            else:
                st.write("目前無最新財經新聞。")

st.sidebar.markdown("---")
st.sidebar.info("提示：若查詢過於頻繁，請稍候再試。")
