import streamlit as st
import json
import os
import pandas as pd
import random

# 設定網頁標題與排版
st.set_page_config(page_title="專業股市決策儀表板", layout="centered")

# CSS 樣式
st.markdown("""
    <style>
    .price-up { color: #ff4b4b; font-weight: bold; font-size: 28px; }
    .price-down { color: #00cc96; font-weight: bold; font-size: 28px; }
    </style>
""", unsafe_allow_html=True)

def normalize_ticker(ticker):
    """將用戶輸入的代號自動標準化為 XXXX.TW"""
    ticker = ticker.strip().upper()
    if not ticker: return ""
    if "." not in ticker:
        # 如果只有數字，補上 .TW
        return f"{ticker}.TW"
    return ticker

def get_simulated_data(ticker):
    # ... (保持原有的擬真數據生成邏輯，確保程式不斷線) ...
    random.seed(hash(ticker) % 100000)
    base_price = round(random.uniform(50, 1000), 1)
    return {"price": base_price, "change": round(random.uniform(-5, 5), 2), "nav": 100, "pe": 20, "eps": 5}

def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {}
    return {}

def main():
    st.title("📈 專業股市決策儀表板")
    
    # 初始化
    if "selected_ticker" not in st.session_state:
        st.session_state.selected_ticker = "2330.TW"

    # 控制面板
    c1, c2 = st.columns([3, 1])
    with c1:
        custom_input = st.text_input("輸入股票代號 (例如: 1301 或 1301.TW):", "")
    with c2:
        st.write("")
        st.write("")
        confirm_btn = st.button("確定選股查詢", use_container_width=True, type="primary")

    if confirm_btn and custom_input.strip():
        # 關鍵修正：執行標準化
        st.session_state.selected_ticker = normalize_ticker(custom_input)
        st.rerun()

    active_ticker = st.session_state.selected_ticker
    st.markdown(f"## 📊 決策報告：**{active_ticker}**")
    
    # 讀取資料
    local_db = load_data()
    if active_ticker in local_db:
        s = local_db[active_ticker]
        st.success(f"✅ 已載入 {active_ticker} 的最新分析數據")
    else:
        s = get_simulated_data(active_ticker)
        st.info("💡 該標的數據庫中暫無記錄，顯示 AI 模擬預測數據。")

    # 顯示數據 (與先前邏輯一致)
    st.metric("即時股價", s.get("price"))
    # ... (其餘版面顯示邏輯)

if __name__ == "__main__":
    main()
