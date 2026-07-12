import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="專業股市決策儀表板", layout="wide")

# 讀取本地靜態檔案，確保永不卡死
@st.cache_data
def load_data():
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

st.title("📈 專業股市決策儀表板")
data = load_data()

# 選擇器
ticker = st.selectbox("選擇監控股票", list(data.keys()) if data else ["2330.TW"])

if ticker in data:
    d = data[ticker]
    # 數值顯示
    cols = st.columns(5)
    cols[0].metric("股價", f"{d.get('price', 0):.2f}")
    cols[1].metric("每股淨值", f"{d.get('nav', 0):.2f}")
    cols[2].metric("本益比", f"{d.get('pe', 0):.2f}")
    cols[3].metric("EPS", f"{d.get('eps', 0):.2f}")
    
    # 預估模型
    st.subheader("📊 財務預估模型")
    st.write(d.get("revenue_forecast", "暫無數據"))
    
    # 圖表
    if "institutional_data" in d:
        df = pd.DataFrame(d["institutional_data"])
        st.line_chart(df.set_index("日期"))
else:
    st.error("找不到市場數據，請檢查 main_task.py 是否已執行並生成 market_data.json。")
