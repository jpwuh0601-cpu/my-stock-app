import streamlit as st
import json
import pandas as pd

# 設定頁面布局
st.set_page_config(page_title="專業股市分析系統", layout="wide")

def load_data():
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def main():
    st.title("📈 專業股市分析系統")
    
    # 載入數據
    data = load_data()
    
    # 側邊欄輸入
    ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
    
    if st.sidebar.button("查詢分析數據"):
        if ticker not in data:
            st.error(f"找不到 {ticker} 的資料，請確認每日分析任務是否已執行。")
            return
            
        stock_info = data[ticker]
        
        # 顯示股價資訊
        st.metric("即時股價", f"{stock_info.get('price', 0):.2f}")
        
        # 顯示地緣政治風險 (黑天鵝警示)
        st.subheader("🦢 全球黑天鵝風險評估")
        status = stock_info.get("black_swan_global", "安全")
        reasons = stock_info.get("black_swan_global_reasons", [])
        
        if status == "⚠️ 警示中":
            st.error(f"狀態: {status}")
            for r in reasons:
                st.write(f"- {r}")
        else:
            st.success(f"狀態: {status} (目前地緣政治風險穩定)")

        # 顯示法人數據
        st.subheader("🏛️ 三大法人十日買賣超細項")
        df_inst = pd.DataFrame(stock_info.get("institutional_data", []))
        if not df_inst.empty:
            st.dataframe(df_inst.style.map(lambda x: 'color: red' if isinstance(x, (int, float)) and x > 0 else 'color: green', subset=['外資', '投信', '自營商']))
        else:
            st.info("暫無法人籌碼資料")

        # 顯示財務報表區塊 (穩定處理)
        st.subheader("📅 財務數據摘要")
        st.write(f"上次更新時間: {stock_info.get('last_update', '未知')}")
        
    else:
        st.info("請輸入代號並點擊查詢，以檢視該檔股票的最新分析報告。")

if __name__ == "__main__":
    main()
