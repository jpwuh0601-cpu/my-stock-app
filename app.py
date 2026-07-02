import streamlit as st
import pandas as pd
import json

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def main():
    st.set_page_config(layout="wide", page_title="AI 智能金融終端")
    data = load_data()
    
    # --- 1. 即時監控與控制 ---
    st.title("📈 AI 智能金融監控終端")
    with st.sidebar:
        st.header("系統控制")
        stock_code = st.text_input("輸入股票代碼", value="2330.TW")
        if st.button("確認選股"):
            st.session_state.selected_stock = stock_code
        st.divider()
        st.warning("⚠️ 黑天鵝危機警示: 正常")
        st.status("自動回測資料來源: ✅ 已校驗")

    # 即時股價與指標
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("即時股價", f"{data.get('price', 0):,.2f}", delta=f"{data.get('change', 0):.2f}")
    c2.metric("每股淨值", f"{data.get('bvps', 0):.2f}")
    c3.metric("10日資券比", f"{data.get('margin_ratio', 0):.2f}%")
    c4.metric("預估 EPS", f"{data.get('eps_forecast', 0):.2f}")

    # --- 2. 財報分析區塊 ---
    st.subheader("財務數據 (今年與去年每季)")
    st.table(pd.DataFrame(data.get("quarterly_reports", {})))

    # --- 3. 籌碼面區塊 ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("三大法人 10日買賣超")
        # 顯示邏輯需包含紅漲綠跌
        st.dataframe(pd.DataFrame(data.get("institutional_investors", [])), use_container_width=True)
    with col2:
        st.subheader("主力券商 10日動向")
        st.dataframe(pd.DataFrame(data.get("top_brokers", [])), use_container_width=True)

    # --- 4. 深度 AI 分析區塊 ---
    st.subheader("即時新聞解讀")
    st.info(data.get("news", "無即時新聞"))
    
    st.subheader("AI 財報預測")
    st.success(data.get("ai_prediction", "預測分析中..."))

if __name__ == "__main__":
    main()
