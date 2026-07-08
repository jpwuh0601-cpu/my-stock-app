import streamlit as st
import yfinance as yf
import pandas as pd

# 頁面配置
st.set_page_config(page_title="股市診斷儀表板", layout="wide")

st.title("📈 專業股市決策儀表板 - 診斷模式")

# 側邊欄輸入
ticker_input = st.sidebar.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.sidebar.button("查詢測試"):
    with st.spinner("正在讀取資料..."):
        try:
            # 處理代號
            symbol = ticker_input if ticker_input.endswith(".TW") else f"{ticker_input}.TW"
            
            # 建立物件
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # 顯示資訊 (純文字顯示，避免渲染衝突)
            st.success(f"成功連線至: {symbol}")
            
            st.subheader("核心數據")
            st.write(f"目前股價: {info.get('currentPrice', '未取得')}")
            st.write(f"每股淨值: {info.get('bookValue', '未取得')}")
            st.write(f"本益比: {info.get('trailingPE', '未取得')}")
            st.write(f"EPS: {info.get('trailingEps', '未取得')}")
            
            # 顯示簡單表格檢查是否正常
            st.subheader("除錯數據清單")
            data_sample = {
                "項目": ["股價", "淨值", "本益比", "EPS"],
                "數值": [info.get('currentPrice', 0), info.get('bookValue', 0), info.get('trailingPE', 0), info.get('trailingEps', 0)]
            }
            st.table(pd.DataFrame(data_sample))
            
        except Exception as e:
            st.error(f"系統錯誤: {str(e)}")
            st.info("提示：如果出現錯誤，請確認網路連線或代號是否正確。")
else:
    st.info("請在左側輸入代號並點擊「查詢測試」，若畫面顯示成功，代表您的部署環境完全正常。")
