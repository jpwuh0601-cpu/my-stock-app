import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
import os

# 設定頁面配置
st.set_page_config(layout="wide", page_title="AI 專業金融分析終端")

def load_data(filepath):
    """載入 JSON 資料，加入錯誤處理，防止前端掛起"""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"資料讀取錯誤: {e}")
        return {}

def main():
    st.title("📈 AI 專業金融分析終端")
    
    # 載入資料
    data = load_data("market_data.json")
    history = load_data("backtest_history.json")
    
    # 側邊欄設定
    with st.sidebar:
        st.header("選股設定")
        user_input = st.text_input("輸入股票代號 (例: 2330.TW)", "2330.TW")
        if st.button("確認選股"):
            st.session_state.target = user_input
            st.rerun()
            
    target = st.session_state.get("target", "2330.TW")
    
    # 確保資料存在，若不存在顯示友善訊息而非崩潰
    if target not in data:
        st.warning(f"⚠️ 目前找不到 {target} 的監控數據。請等待自動化任務更新或確認代號是否正確。")
        st.info("若為剛加入的代號，系統會自動在下次排程抓取。")
        return

    info = data[target]

    # 1. 即時股價
    st.header(f"1. 即時股價: {target}")
    price = info.get("price", 0)
    prev = info.get("prev_close", 0)
    diff = round(float(price) - float(prev), 2)
    st.metric("當前價格", f"{price} 元", delta=f"{diff} 元")

    # 2. 基本面數據
    st.subheader("2. 基本面數據")
    c1, c2, c3 = st.columns(3)
    c1.metric("每股淨值 (NAV)", info.get("nav", "N/A"))
    c2.metric("本益比 (P/E)", info.get("pe", "N/A"))
    c3.metric("EPS", info.get("eps", "N/A"))

    # 5. 三大法人買賣超 (修正棄用警告)
    st.subheader("5. 三大法人買賣超")
    if "institutional_daily" in info:
        st.dataframe(pd.DataFrame(info["institutional_daily"]), use_container_width=True)
    
    # 6. 資券比與主力券商 (修正棄用警告)
    st.subheader("6. 10日資券比與主力券商")
    if "broker_daily" in info:
        st.dataframe(pd.DataFrame(info["broker_daily"]), use_container_width=True)

    # 7. AI 分析
    st.subheader("7. AI 分析與績效統計")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.info(f"📰 GPT 新聞解讀: {info.get('news_analysis', '暫無近期新聞')}")
        st.success(f"🤖 AI 財報預測: {info.get('ai_prediction', '分析中...')}")
    with col_b:
        st.metric("🤖 AI 歷史勝率", info.get("win_rate", "0%"))

    # 繪製圖表
    st.subheader("📊 AI 預測績效走勢圖")
    if target in history and "prices" in history[target]:
        prices = history[target]["prices"]
        fig = go.Figure(data=go.Scatter(y=prices, mode='lines+markers', line=dict(color='firebrick', width=2)))
        fig.update_layout(title="歷史回測股價走勢", xaxis_title="更新次數", yaxis_title="價格 (元)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("尚無足夠歷史數據繪製圖表")

if __name__ == "__main__":
    main()
