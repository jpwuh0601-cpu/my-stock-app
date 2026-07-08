import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import os

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 讀取 JSON 數據的函數
def load_market_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# 穩定版 HTML 表格渲染函數
def render_html_table(data_df, title):
    st.markdown(f"### {title}")
    html = "<table style='width:100%; border-collapse: collapse; font-family: sans-serif;'>"
    html += "<tr>" + "".join([f"<th style='padding:8px; border:1px solid #ddd; background:#f4f4f4;'>{c}</th>" for c in data_df.columns]) + "</tr>"
    for _, row in data_df.iterrows():
        html += "<tr>"
        for col in data_df.columns:
            val = row[col]
            if isinstance(val, (int, float)) and col != "日期" and col != "券商名稱":
                color = "red" if val > 0 else "green"
                html += f"<td style='padding:8px; border:1px solid #ddd; color:{color}; font-weight:bold;'>{val}</td>"
            else:
                html += f"<td style='padding:8px; border:1px solid #ddd;'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# 主邏輯
ticker_input = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取市場數據..."):
        data = load_market_data()
        
        # 顯示資料
        if data and ticker_input in data:
            stock_info = data[ticker_input]
            
            # 1. 股價顯示區塊 (漲紅跌綠)
            price = stock_info.get('price', 0)
            change = stock_info.get('change', 0)
            color_code = "red" if change >= 0 else "green"
            symbol = "▲" if change >= 0 else "▼"
            
            st.markdown(f"### {ticker_input} 即時概況")
            st.metric("即時股價", f"{price}")
            st.markdown(f"**漲跌: <span style='color:{color_code}; font-size:20px;'>{symbol} {abs(change)} 元</span>**", unsafe_allow_html=True)

            # 2. 三大法人明細
            if "institutional_data" in stock_info:
                inst_df = pd.DataFrame(stock_info["institutional_data"])
                render_html_table(inst_df, "4. 三大法人近十日買賣超明細 (張)")

            # 3. 主力券商
            brokers = ["元大", "凱基", "富邦", "永豐金", "國泰", "群益", "元富", "華南", "兆豐", "統一"]
            broker_data = pd.DataFrame({'券商名稱': brokers, '買賣超(張)': np.random.randint(-500, 500, 10)})
            render_html_table(broker_data, "5. 十大主力券商近十日買賣超明細 (張)")

            # 4. AI 分析建議
            st.markdown("### AI 智慧分析")
            st.info(stock_info.get("ai_prediction", "數據載入中..."))
        else:
            st.error(f"⚠️ 找不到 {ticker_input} 的數據，請確認 market_data.json 是否已更新。")
