import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
import os
import time

# 設定頁面配置
st.set_page_config(layout="wide", page_title="AI 專業金融分析終端")

def load_data(filepath):
    """載入 JSON 資料，加入多重錯誤處理"""
    if not os.path.exists(filepath):
        return {}
    try:
        # 增加短暫延遲防止檔案並發寫入衝突
        time.sleep(0.1)
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"資料讀取失敗: {e}")
        return {}

def main():
    st.title("📈 AI 專業金融分析終端")
    
    # 載入數據
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
    
    # 針對 JSON 損毀或遺失資料的防禦處理
    if not data or target not in data:
        st.warning(f"⚠️ 找不到 {target} 的數據，或資料庫初始化中。")
        st.info("請確認 GitHub Actions 自動化任務是否已執行完畢。")
        return

    info = data[target]

    # --- 儀表板區塊 ---
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header(f"即時股價: {target}")
        price = info.get("price", 0)
        prev = info.get("prev_close", 0)
        diff = round(float(price) - float(prev), 2)
        st.metric("當前價格", f"{price} 元", delta=f"{diff} 元")

    with col2:
        st.header("基本面摘要")
        c1, c2, c3 = st.columns(3)
        c1.metric("淨值 (NAV)", info.get("nav", "N/A"))
        c2.metric("本益比 (P/E)", info.get("pe", "N/A"))
        c3.metric("EPS", info.get("eps", "N/A"))

    # 籌碼與分析
    st.divider()
    st.subheader("籌碼與績效指標")
    
    # 使用 width=None 避免棄用警告
    if "institutional_daily" in info:
        st.write("三大法人買賣超：")
        st.dataframe(pd.DataFrame(info["institutional_daily"]), width=None)

    # AI 績效
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("🤖 AI 歷史回測勝率", info.get("win_rate", "0%"))
    
    # 繪製圖表
    st.subheader("📊 AI 預測績效走勢")
    if target in history and "prices" in history[target]:
        prices = history[target]["prices"]
        fig = go.Figure(data=go.Scatter(y=prices, mode='lines+markers', line=dict(color='blue', width=2)))
        fig.update_layout(height=400, xaxis_title="時間序列", yaxis_title="價格")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("尚無足夠回測數據。")

if __name__ == "__main__":
    main()
