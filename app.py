import streamlit as st
import yfinance as yf

# 設定頁面資訊
st.set_page_config(page_title="股票即時分析", layout="centered")

# 使用新的函式名稱與結構，並加上快取過期設定
@st.cache_data(ttl=300)
def fetch_stock_info(ticker):
    """
    抓取指定股票代號的即時資訊
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        # 確保回傳一個非空的字典
        if not info or "currentPrice" not in info:
            return {"error": "無法獲取股價，請檢查代號是否正確。"}
        return info
    except Exception as e:
        return {"error": str(e)}

st.title("📊 股票即時分析器")

# 輸入框
ticker_input = st.text_input("請輸入股票代號 (例如: 2330.TW)", "2330.TW")

# 按鈕與執行邏輯
if st.button("開始查詢"):
    with st.spinner("正在讀取資料..."):
        # 確保只傳遞 ticker 一個參數
        result = fetch_stock_info(ticker_input)
        
        # 判斷是否出錯
        if isinstance(result, dict) and "error" in result:
            st.error(f"⚠️ {result['error']}")
        else:
            # 顯示結果
            current_price = result.get("currentPrice", "N/A")
            company_name = result.get("longName", "未知公司")
            
            st.success(f"查詢成功！")
            st.metric(label=f"{company_name} 目前股價", value=f"{current_price} TWD")
            
            # 若想查看詳細資訊，可選用 st.json
            with st.expander("查看原始資料細節"):
                st.json(result)
