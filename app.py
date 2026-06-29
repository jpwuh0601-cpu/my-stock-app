import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="專業投資決策儀表板", layout="wide")

st.title("📈 專業投資決策儀表板")

# 假設資料已透過 GitHub Actions 更新並儲存於 market_data.json
def load_data():
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

data = load_data()

if data:
    # 1 & 2. 即時指標 (Row 1)
    col1, col2 = st.columns(2)
    col1.metric("即時股價", f"${data.get('price', 0)}")
    col2.metric("每股淨值 (BVPS)", f"${data.get('bvps', 0)}")

    st.divider()

    # 版面分頁
    tab1, tab2, tab3 = st.tabs(["財務與績效", "籌碼面分析", "AI 預測與新聞"])

    with tab1:
        st.subheader("每季財報報表")
        st.table(pd.DataFrame(data.get('financials', {})))
        st.write(f"預估今年 EPS: {data.get('est_eps')} | 預估股利: {data.get('est_dividend')}")

    with tab2:
        st.subheader("三大法人買賣超 (近10日)")
        # 籌碼面邏輯：紅買綠賣
        df_inst = pd.DataFrame(data.get('institutional_investors', []))
        def color_negative_red(val):
            color = 'red' if val > 0 else 'green'
            return f'color: {color}'
        st.dataframe(df_inst.style.applymap(color_negative_red, subset=['買賣超']))

        st.subheader("10日資券比")
        st.write(f"資券比: {data.get('margin_ratio')}%")

    with tab3:
        st.subheader("最新市場新聞")
        for news in data.get('news', []):
            st.write(f"• {news}")
        
        st.subheader("AI 財報預測")
        st.info(data.get('ai_prediction'))

else:
    st.warning("數據更新中，請稍候...")
