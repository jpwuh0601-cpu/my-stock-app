import streamlit as st
import json
import pandas as pd
import plotly.express as px
import os
from datetime import datetime, timedelta

# 設定版面
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    if not os.path.exists("market_data.json"):
        return {}
    with open("market_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def check_data_freshness(last_updated_str):
    try:
        last_updated = datetime.strptime(last_updated_str, "%Y-%m-%d %H:%M:%S")
        if datetime.now() - last_updated > timedelta(hours=24):
            return False, "數據來源已過期 (超過24小時)，請觸發自動化更新。"
        return True, "數據更新正常。"
    except:
        return False, "無法讀取回測時間戳記。"

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    # 檢查回測正確性
    is_fresh, status_msg = check_data_freshness(data.get("last_updated", "2000-01-01 00:00:00"))
    if not is_fresh:
        st.error(f"⚠️ 系統錯誤: {status_msg}")

    # 側邊欄選擇
    tickers = [t for t in data.keys() if t != "last_updated"]
    selected_ticker = st.sidebar.selectbox("請選擇股票代號", tickers)
    submit = st.sidebar.button("確定分析")

    if submit:
        info = data.get(selected_ticker, {})
        
        # 1. 即時股價與漲跌 (漲紅跌綠)
        price = float(info.get("price", 0))
        st.header(f"監控目標: {selected_ticker}")
        st.metric("即時股價", f"{price:,.2f}")

        # 2. 財報欄位 (BVPS, PE, EPS)
        col1, col2, col3 = st.columns(3)
        col1.metric("每股淨值 (BVPS)", f"{info.get('bvps', 0):,.2f}")
        col2.metric("本益比 (PE)", f"{info.get('pe', 0):,.2f}")
        col3.metric("EPS", f"{info.get('eps', 0):,.2f}")

        st.divider()

        # 3. 走勢圖與 AI 分析
        history = info.get("history", [])
        if history:
            df = pd.DataFrame(history)
            fig = px.line(df, x="Date", y="Close", title=f"{selected_ticker} 走勢圖")
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("🤖 AI 財報預測分析")
        st.info(info.get("ai_prediction", "暫無分析"))

if __name__ == "__main__":
    main()
