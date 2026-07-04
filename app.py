import streamlit as st
import json
import os
import pandas as pd

# 頁面配置：強制寬版顯示，固定面板邏輯
st.set_page_config(layout="wide", page_title="專業金融監控終端")

def load_data(filepath):
    if not os.path.exists(filepath): return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f: return json.load(f)
    except: return {}

def main():
    st.title("📈 專業金融監控終端")
    data = load_data("market_data.json")
    
    # --- 1. 側邊欄選股與固定配置 ---
    with st.sidebar:
        st.header("監控面板設定")
        tickers = list(data.keys()) if data else []
        selected_ticker = st.selectbox("請選擇監控標的：", tickers)
        if st.button("固定該標的"):
            st.session_state.target = selected_ticker
            st.rerun()

    target = st.session_state.get("target", "2330.TW")
    info = data.get(target, {})

    # --- 2. 即時資訊區塊 (固定於最上方) ---
    st.subheader(f"標的: {target}")
    price = info.get("price", 0)
    change = info.get("change", 0)
    
    # 漲紅跌綠邏輯
    color = "normal" if change == 0 else ("inverse" if change > 0 else "normal")
    st.metric("即時股價", f"{price} 元", delta=f"{change} 元")

    # --- 3. 財務指標面板 (模組化 Grid) ---
    c1, c2, c3 = st.columns(3)
    c1.metric("每股淨值", info.get("nav", "N/A"))
    c2.metric("本益比", info.get("pe", "N/A"))
    c3.metric("EPS", info.get("eps", "N/A"))

    # --- 4. 預留區塊：AI 財報預測與即時新聞 ---
    # 此區塊會隨著後續資料擴充自動延伸
    with st.container():
        st.subheader("🤖 AI 財報與趨勢預測")
        st.info(info.get("ai_prediction", "分析中..."))
        st.write("即時新聞動態：(待接通 API...)")

    # --- 5. 籌碼分析區塊 (預留資券比與法人買賣超位置) ---
    with st.container():
        st.subheader("籌碼與主力動向")
        c_a, c_b = st.columns(2)
        c_a.metric("10日資券比", f"{info.get('margin_ratio', 0)}%")
        c_b.write("主力券商動向：(待擴充...)")

    # --- 6. 財報報表與回測區塊 ---
    with st.expander("展開：查看今年與去年詳細報表"):
        st.write("報表數據區塊已就緒，請在 worker.py 加入對應 JSON 欄位。")

if __name__ == "__main__":
    main()
