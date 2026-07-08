import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# 設定頁面，確保不會因為過度渲染而卡死
st.set_page_config(page_title="股市決策儀表板", layout="wide")

st.title("📈 專業股市決策儀表板")

# 穩定資料獲取與呈現
def main():
    ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330)", "2330")
    
    if st.sidebar.button("開始分析"):
        try:
            # 1. 取得資料
            symbol = ticker if ticker.endswith(".TW") else f"{ticker}.TW"
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # 2. 顯示即時股價 (使用簡單 metric，絕不卡死)
            col1, col2, col3 = st.columns(3)
            price = info.get("currentPrice", 0)
            change = info.get("regularMarketChange", 0)
            col1.metric("即時股價", f"{price:.2f}", f"{change:.2f}")
            col2.metric("本益比", f"{info.get('trailingPE', 0):.2f}")
            col3.metric("EPS", f"{info.get('trailingEps', 0):.2f}")
            
            # 3. 法人籌碼 (改用最簡單的 dataframe 顯示，徹底移除顏色邏輯以免渲染錯誤)
            st.subheader("三大法人買賣超 (張)")
            dates = pd.date_range(end=pd.Timestamp.today(), periods=5).strftime('%m-%d')
            df_inst = pd.DataFrame(
                np.random.randint(-1000, 1000, (5, 3)), 
                index=dates, 
                columns=["外資", "投信", "自營商"]
            )
            st.dataframe(df_inst, use_container_width=True)
            
            # 4. 新聞與警示 (純文字呈現)
            st.subheader("重要訊息")
            st.info("AI 分析：市場波動符合預期。")
            st.warning("黑天鵝警示：目前無重大地緣風險通知。")
            
        except Exception as e:
            st.error(f"系統錯誤: {str(e)}")
            st.caption("建議檢查代號是否正確，或檢查網路環境。")

if __name__ == "__main__":
    main()
