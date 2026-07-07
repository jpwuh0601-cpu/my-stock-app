import streamlit as st
import json
import pandas as pd

# 設定頁面風格
st.set_page_config(page_title="專業股市分析系統", layout="wide")

@st.cache_data(ttl=3600)
def load_data():
    """讀取市場分析數據"""
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {}

def main():
    st.title("📈 專業股市分析系統")
    
    data = load_data()
    
    # 側邊欄：選擇股票
    ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
    
    if st.sidebar.button("查詢分析數據"):
        if ticker not in data:
            st.error(f"找不到 {ticker} 的資料，請確認 GitHub Actions 是否已更新 market_data.json")
            return
            
        stock_info = data[ticker]
        
        # 1. 股價與基本資訊
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("即時股價", f"{stock_info.get('price', 0):.2f}")
        
        # 2. 地緣政治黑天鵝風險 (來自 analyzer.py 的分析)
        st.subheader("🦢 全球黑天鵝風險評估")
        status = stock_info.get("black_swan_global", "安全")
        reasons = stock_info.get("black_swan_global_reasons", [])
        
        if status == "⚠️ 警示中":
            st.error(f"狀態: {status}")
            for r in reasons:
                st.write(f"- {r}")
        else:
            st.success(f"狀態: {status} (目前地緣政治風險穩定)")

        # 3. 法人數據
        st.subheader("🏛️ 三大法人十日買賣超細項")
        df_inst = pd.DataFrame(stock_info.get("institutional_data", []))
        if not df_inst.empty:
            st.dataframe(df_inst.style.map(lambda x: 'color: red' if isinstance(x, (int, float)) and x > 0 else 'color: green', subset=['外資', '投信', '自營商']))
        else:
            st.info("暫無籌碼資料")

        st.write(f"最後更新時間: {stock_info.get('last_update', '未知')}")
        
    else:
        st.info("請在左側輸入代號並點擊「查詢分析數據」。")

if __name__ == "__main__":
    main()
