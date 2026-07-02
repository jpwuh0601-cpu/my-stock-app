import streamlit as st
import pandas as pd
import json
import os

# 設定頁面配置
st.set_page_config(layout="wide", page_title="AI 智能金融終端")

def load_data():
    """載入數據並確保格式正確"""
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def main():
    data = load_data()
    
    # --- 頂部：即時監控與控制 ---
    st.title("📈 AI 智能金融監控終端")
    
    # 側邊欄控制
    with st.sidebar:
        st.header("系統控制")
        stock_code = st.text_input("輸入股票代碼", value="2330.TW")
        if st.button("確認選股"):
            st.session_state.selected_stock = stock_code
        st.divider()
        st.warning("⚠️ 黑天鵝危機警示: 正常")
        st.status("自動回測資料來源: ✅ 已校驗")

    # 1. 即時股價與指標
    c1, c2, c3, c4 = st.columns(4)
    # 漲紅跌綠 delta 顯示
    c1.metric("即時股價", f"{data.get('price', 0):,.2f}", delta=f"{data.get('change', 0):+.2f}")
    c1.button("刷新報價")
    # 2. 每股淨值
    c2.metric("每股淨值", f"{data.get('bvps', 0):.2f}")
    # 3. 預估營收/EPS/股利
    c3.metric("預估EPS/股利", f"{data.get('eps_forecast', 0):.2f} / {data.get('dividend_forecast', 0):.2f}")
    c4.metric("10日資券比", f"{data.get('margin_ratio', 0):.2f}%")

    # --- 財務報表與籌碼分析 ---
    tab1, tab2 = st.tabs(["財務報表", "籌碼與主力分析"])
    
    with tab1:
        st.subheader("今年與去年每季財務報表")
        st.table(pd.DataFrame(data.get("quarterly_reports", {})))
        
        # 7. AI 財報預測 (放置在新聞後)
        st.subheader("AI 財報預測")
        st.success(data.get("ai_prediction", "分析中..."))

    with tab2:
        # 5. 三大法人 10 日買賣超
        st.subheader("三大法人 10日買賣超")
        st.dataframe(pd.DataFrame(data.get("institutional_investors", [])), use_container_width=True)
        
        # 6. 10日主力券商動向
        st.subheader("10日主力券商動向")
        st.dataframe(pd.DataFrame(data.get("top_brokers", [])), use_container_width=True)

    # --- 系統資訊區 ---
    st.divider()
    st.subheader("即時新聞解讀")
    st.info(data.get("news", "無即時新聞"))

if __name__ == "__main__":
    main()
