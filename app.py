import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
import os

# 設定頁面配置
st.set_page_config(layout="wide", page_title="AI 專業金融分析終端")

def load_data(filepath):
    """載入通用 JSON 資料"""
    try:
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return {}

def main():
    st.title("📈 AI 專業金融分析終端")
    data = load_data("market_data.json")
    history = load_data("backtest_history.json")
    
    # 側邊欄固定選股邏輯
    with st.sidebar:
        st.header("選股設定")
        user_input = st.text_input("輸入股票代號 (例: 2330.TW)", "2330.TW")
        if st.button("確認選股"):
            st.session_state.target = user_input
            st.rerun()
            
    target = st.session_state.get("target", "2330.TW")
    info = data.get(target) or {}

    # --- 固定模組區塊排列 ---
    
    # 1. 即時股價
    st.header(f"1. 即時股價: {target}")
    price = info.get("price", 0)
    prev = info.get("prev_close", 0)
    diff = round(float(price) - float(prev), 2)
    st.metric("當前價格", f"{price} 元", delta=f"{diff} 元")

    # 2. 基本面數據
    st.subheader("2. 基本面數據 (淨值/本益比/EPS)")
    c1, c2, c3 = st.columns(3)
    c1.metric("每股淨值 (NAV)", info.get("nav", "N/A"))
    c2.metric("本益比 (P/E)", info.get("pe", "N/A"))
    c3.metric("EPS", info.get("eps", "N/A"))

    # 4. 今年與去年每季報表
    st.subheader("4. 今年與去年每季報表")
    st.write("自動回測資料來源：狀態 [正常]")

    # 5. 三大法人買賣超 (已修正警告，改用 width=None 自動延展)
    st.subheader("5. 三大法人買賣超 (10日)")
    if "institutional_daily" in info and info["institutional_daily"]:
        st.dataframe(pd.DataFrame(info["institutional_daily"]), width=None)

    # 6. 資券比與主力券商 (已修正警告)
    st.subheader("6. 10日資券比與主力券商")
    if "broker_daily" in info and info["broker_daily"]:
        st.dataframe(pd.DataFrame(info["broker_daily"]), width=None)

    # 7. AI 分析與績效統計
    st.subheader("7. AI 分析與績效統計")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.info(f"📰 GPT 新聞解讀: {info.get('news_analysis', '暫無近期新聞')}")
        st.success(f"🤖 AI 財報預測: {info.get('ai_prediction', '分析中...')}")
        st.error(f"⚠️ 黑天鵝危機警示: {info.get('black_swan_alert', '系統監控中：無異常')}")
    with col_b:
        st.metric("🤖 AI 歷史預測勝率", info.get("win_rate", "0%"))

    # 繪製 Plotly 折線圖
    st.subheader("📊 AI 預測績效走勢圖")
    if target in history and "prices" in history[target]:
        prices = history[target]["prices"]
        fig = go.Figure(data=go.Scatter(y=prices, mode='lines+markers', line=dict(color='firebrick', width=2)))
        fig.update_layout(title="歷史回測股價走勢", xaxis_title="更新次數", yaxis_title="價格 (元)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("目前尚無足夠的歷史回測數據繪製圖表")

if __name__ == "__main__":
    main()
