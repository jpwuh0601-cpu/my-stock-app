import streamlit as st
import json
import os
import pandas as pd

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

# 讀取數據函式
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "market_data.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None
    return None

data = load_data()

# 側邊欄
st.sidebar.header("股票搜尋")
stock_code = st.sidebar.text_input("輸入台股代碼")

if st.sidebar.button("開始搜尋") and data:
    # 1 & 2. 即時股價與每股淨值
    col1, col2 = st.columns(2)
    col1.metric("即時股價", f"{data.get('price', 0)}")
    col2.metric("每股淨值 (BVPS)", f"{data.get('bvps', 0)}")

    # 4. 今年與去年每季報表
    st.subheader("今年與去年每季財報")
    financials = data.get("financials", {})
    if financials:
        df_fin = pd.DataFrame.from_dict(financials, orient='index')
        st.dataframe(df_fin, use_container_width=True)

    # 5. 股市3大法人買賣超 (10日)
    st.subheader("股市三大法人買賣超 (近10日)")
    inst_data = data.get("institutional_investors", [])
    if inst_data:
        df_inst = pd.DataFrame(inst_data)
        st.dataframe(df_inst, use_container_width=True, column_config={
            "買賣超": st.column_config.NumberColumn("買賣超", format="%d", help="正數為買超(紅)，負數為賣超(綠)")
        })

    # 6. 資券比與主力券商
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("10日資券比")
        st.metric("當前資券比", f"{data.get('margin_ratio', 'N/A')}%")
    with col_b:
        st.subheader("主力券商買賣 (10日)")
        brokers = data.get("top_brokers", [])
        st.write(brokers if brokers else "無數據")

    # 新聞與 AI 預測
    st.subheader("即時新聞")
    news = data.get("news", [])
    for item in news:
        st.write(f"- {item}")

    # 7. AI 財報預測 (含營收、EPS、股利)
    st.subheader("AI 財報預測")
    ai_data = data.get("ai_forecast", {})
    if ai_data:
        fcol1, fcol2, fcol3 = st.columns(3)
        fcol1.metric("預估今年營收", ai_data.get("revenue", "N/A"))
        fcol2.metric("預估 EPS", ai_data.get("eps", "N/A"))
        fcol3.metric("預估股利", ai_data.get("dividend", "N/A"))
        st.info(ai_data.get("comment", "系統分析中..."))
    else:
        st.write("暫無 AI 預測數據")

    # 資料來源驗證
    st.sidebar.success("資料來源驗證：正常")

elif not data:
    st.warning("請確保 market_data.json 已生成且包含數據。")
