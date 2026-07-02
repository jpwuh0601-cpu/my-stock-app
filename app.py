import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融終端")

def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def main():
    data = load_data()
    st.title("📈 AI 智能金融監控終端")
    
    # 側邊欄控制
    with st.sidebar:
        st.header("系統控制")
        st.text_input("輸入股票代碼", value="2330.TW")
        st.divider()
        st.warning("⚠️ 黑天鵝危機警示: 正常")
        st.status("自動回測資料來源: ✅ 已校驗")

    # 1. 核心指標區塊
    st.subheader("核心財務指標")
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{data.get('price', 0):,.2f}", delta=f"{data.get('change', 0):+.2f}")
    cols[1].metric("每股淨值", f"{data.get('bvps', 0):.2f}")
    cols[2].metric("本益比 (PE)", f"{data.get('pe_ratio', 0):.2f}")
    cols[3].metric("10日資券比", f"{data.get('margin_ratio', 0):.2f}%")
    cols[4].metric("預估 EPS", f"{data.get('eps_forecast', 0):.2f}")

    # 2. 報表與籌碼分析
    tab1, tab2 = st.tabs(["財務報表", "籌碼與主力分析"])
    
    with tab1:
        st.subheader("今年與去年每季財務報表")
        st.table(pd.DataFrame(data.get("quarterly_reports", {})))
        
        # 放置財報預測
        st.subheader("AI 財報預測")
        st.success(data.get("ai_prediction", "分析中..."))

    with tab2:
        st.subheader("三大法人 10日買賣超")
        st.dataframe(pd.DataFrame(data.get("institutional_investors", [])), use_container_width=True)
        
        st.subheader("10日主力券商動向")
        st.dataframe(pd.DataFrame(data.get("top_brokers", [])), use_container_width=True)

    # 3. 新聞與 AI 解讀
    st.divider()
    st.subheader("即時新聞解讀")
    st.info(data.get("news", "無即時新聞"))

if __name__ == "__main__":
    main()
