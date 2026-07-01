import streamlit as st
import pandas as pd
import json
import os
import plotly.graph_objects as go

# 頁面配置
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

def load_market_data():
    """安全讀取 JSON 資料"""
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if data is not None else {}
        except Exception:
            return {}
    return {}

data = load_market_data()

# 在存取數據前增加檢查，避免 NoneType 錯誤
if not data:
    st.warning("數據尚未載入或格式異常，請稍候。")
else:
    # 使用 .get() 提供預設值，避免 Key Error 或 NoneType Error
    price = data.get('price', 0)
    pe = data.get('pe_ratio', 'N/A')
    eps = data.get('trailing_eps', 'N/A')
    
    col1, col2, col3 = st.columns(3)
    col1.metric("即時股價", f"${price:,.2f}")
    col2.metric("本益比", pe)
    col3.metric("每股盈餘", eps)

    # 籌碼面檢查
    st.subheader("籌碼面資訊")
    investors = data.get('institutional_investors')
    if isinstance(investors, list) and len(investors) > 0:
        st.write(f"機構動向: {investors[0].get('機構', '未知')}, 買賣超: {investors[0].get('買賣超', 0)}")
    else:
        st.write("目前無外資籌碼數據。")
