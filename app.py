import streamlit as st
import json

# 極致簡化的配置，避免複雜組件衝突
st.set_page_config(page_title="股市儀表板", layout="wide")

st.title("📈 股市決策儀表板")

# 使用簡單的本地讀取，不執行任何複雜運算
try:
    with open("market_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except:
    data = {}

# 簡單的下拉選擇
ticker = st.selectbox("請選擇股票", list(data.keys()) if data else ["請先執行 main_task.py"])

if ticker in data:
    d = data[ticker]
    # 使用最基礎的元件顯示
    st.metric("股價", d.get("price", 0))
    st.write("數據來源: market_data.json")
else:
    st.write("等待數據更新...")
