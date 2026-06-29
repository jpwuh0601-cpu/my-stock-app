import streamlit as st
import json
import pandas as pd
import os

# 設定頁面為寬版模式
st.set_page_config(page_title="AI 投資決策儀表板", layout="wide")

st.title("📊 AI 投資決策儀表板")

# 讀取 JSON 資料的函式
def load_data():
    file_path = "market_data.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

data = load_data()

if data:
    # 建立指標卡片
    col1, col2 = st.columns(2)
    col1.metric("即時股價", f"{data['price']}", delta=f"{data['change']}%")
    col2.metric("每股淨值", f"{data['bvps']}")
    
    # 建立分頁視覺化
    tab1, tab2 = st.tabs(["法人籌碼分析", "AI 市場觀點"])
    
    with tab1:
        st.subheader("三大法人買賣超")
        df = pd.DataFrame(data['institutional_investors'])
        st.table(df)
        
    with tab2:
        st.subheader("AI 市場分析")
        st.info(data['ai_prediction'])
        st.write("最新市場新聞:", ", ".join(data['news']))

else:
    st.warning("正在等待自動化任務產出數據，請稍候...")
