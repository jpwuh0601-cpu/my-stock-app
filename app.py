import streamlit as st
import pandas as pd
import json
import os
from analyzer import generate_ai_analysis

# 設定網頁版面
st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_data():
    """讀取自動化產生的 JSON 檔案"""
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 側邊欄輸入
ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    data = load_data()
    d = data.get(ticker)
    
    if not d:
        st.error(f"查無 '{ticker}' 資料，請確認 Actions 已成功更新 JSON。")
    else:
        # 1 & 2. 財務數據排版
        st.subheader("1 & 2. 基本財務數據")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("即時股價", d.get('price', '0'))
        c2.metric("每股淨額 (NAV)", d.get('nav', '0'))
        c3.metric("本益比 (PE)", d.get('pe', '0'))
        c4.metric("每股盈餘 (EPS)", d.get('eps', '0'))

        # 3. 每季報表
        st.subheader("3. 歷史每季報表")
        st.info(d.get("quarterly_report", "目前無季度報表資料"))

        # 4. 法人買賣超 (紅漲綠跌邏輯)
        st.subheader("4. 三大法人十日買賣超")
        inst_data = d.get("institutional_data", [])
        if inst_data:
            df = pd.DataFrame(inst_data)
            # 顏色條件渲染
            def color_negative_red(val):
                color = 'red' if float(val) > 0 else 'green'
                return f'color: {color}'
            st.dataframe(df.style.applymap(color_negative_red, subset=['外資', '投信', '自營商']))
        
        # 5. 資券比
        st.subheader("5. 資券比與主力券商")
        st.write(d.get("margin_trading", "資料更新中..."))

        # 8. 即時新聞
        st.subheader("8. 即時新聞")
        st.write(d.get("news", "無最新消息"))

        # 6. AI 財報預測
        st.subheader("6. AI 財報預測")
        ai_res = d.get("ai_prediction", "")
        if "分析中" in ai_res:
            with st.spinner("AI 正在分析數據..."):
                # 這裡調用 analyzer.py
                ai_res = generate_ai_analysis(ticker, d, inst_data)
                st.success(ai_res.get("main_force_analysis"))
        else:
            st.success(ai_res)

        # 7. 年度預估
        st.subheader("7. 年度預估")
        st.write(d.get("annual_forecast", "分析中..."))
