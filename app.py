import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="AI 金融監控中心")

def load_data():
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def main():
    st.sidebar.title("🔍 選股與監控")
    ticker_input = st.sidebar.text_input("輸入股票代號 (例: 2330.TW)")
    
    data = load_data()
    # 支援輸入與既有列表
    sym = ticker_input if ticker_input else list(data.keys())[0] if data else "2330.TW"
    info = data.get(sym, {})

    st.title(f"📊 {sym} 即時監控儀表板")
    
    # 1. 即時股價與漲跌 (紅綠標示)
    diff = info.get("price", 0) - info.get("prev_close", 0)
    delta_text = f"{diff:+.2f} 元"
    st.metric("即時股價", f"{info.get('price', 0)} 元", delta=delta_text)

    # 2. 功能區塊
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚠️ 黑天鵝危機警示")
        st.error(info.get("black_swan_alert", "系統監控中：無異常"))
    with col2:
        st.subheader("🤖 AI 選股建議")
        st.info(info.get("ai_stock_pick", "分析中..."))

    # 3. 三大法人與主力分析
    st.subheader("🧠 AI 主力分析與外資動向")
    if "institutional_daily" in info:
        st.dataframe(pd.DataFrame(info["institutional_daily"]))
    
    st.subheader("📰 GPT 新聞解讀")
    st.write(info.get("news_analysis", "無近期新聞"))

if __name__ == "__main__":
    main()
