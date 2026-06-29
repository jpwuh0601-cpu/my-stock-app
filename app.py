import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="專業投資決策儀表板", layout="wide")

st.title("📈 專業投資決策儀表板")

def load_data():
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

data = load_data()

if data:
    # 1. Row 1: 即時股價與每股淨值
    col1, col2 = st.columns(2)
    col1.metric("即時股價", f"${data.get('price', 0)}")
    col2.metric("每股淨值 (BVPS)", f"${data.get('bvps', 0)}")

    st.divider()

    # 2. 分頁版面
    tab1, tab2, tab3 = st.tabs(["財務與績效", "籌碼面分析", "AI 預測與市場動態"])

    with tab1:
        st.subheader("每季財報報表")
        st.table(pd.DataFrame(data.get('financials', {})))
        
        st.subheader("年度財務預估")
        # 顯示預估營收、EPS與股利
        f_col1, f_col2, f_col3 = st.columns(3)
        f_col1.metric("預估今年營收", f"{data.get('est_revenue', 'N/A')}")
        f_col2.metric("預估 EPS", f"{data.get('est_eps', 'N/A')}")
        f_col3.metric("預估股利", f"{data.get('est_dividend', 'N/A')}")

    with tab2:
        st.subheader("三大法人買賣超 (近10日)")
        df_inst = pd.DataFrame(data.get('institutional_investors', []))
        
        # 紅買綠賣邏輯
        def color_map(val):
            return f'color: {"red" if val > 0 else "green"}'
        
        if not df_inst.empty:
            st.dataframe(df_inst.style.applymap(color_map, subset=['買賣超']))
        
        st.subheader("10日資券比")
        st.metric("資券比", f"{data.get('margin_ratio', 0)}%")
        
        st.subheader("主力券商買賣")
        st.write(data.get('top_brokers', '無即時數據'))

    with tab3:
        st.subheader("最新市場新聞")
        for news in data.get('news', []):
            st.write(f"• {news}")
            
        st.subheader("AI 財報預測")
        st.info(data.get('ai_prediction', '無預測數據'))

else:
    st.warning("數據更新中，請稍候...")
