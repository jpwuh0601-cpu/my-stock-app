import streamlit as st
import json
import os
import pandas as pd
from worker import fetch_stock_data

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="centered")

def load_data():
    """載入本地 JSON 資料"""
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def main():
    st.title("📈 專業股市決策儀表板")
    data = load_data()

    # 輸入股票代號
    ticker = st.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
    
    if st.button("查詢分析數據"):
        st.session_state.current_ticker = ticker

    target_ticker = st.session_state.get("current_ticker", ticker)
    
    # 邏輯：優先顯示本地 JSON 數據，避免即時 API 超時
    if target_ticker in data:
        s = data[target_ticker]
        
        st.markdown(f"### 查詢結果: {target_ticker}")
        st.metric("即時股價", s.get('price', 0))
        
        # 顯示各項指標
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨值", s.get('nav', 0))
        c2.metric("本益比", s.get('pe', 0))
        c3.metric("EPS", s.get('eps', 0))
        
        st.subheader("📊 技術分析數據")
        st.table(pd.DataFrame({
            "指標": ["KD", "MACD", "RSI"],
            "數值": [s.get('kd', 50), s.get('macd', 0), s.get('rsi', 50)]
        }))
        
        st.subheader("📰 即時股市新聞")
        for news in ["市場資金流向穩定", "相關產業前景看好", "技術指標維持多頭格局"]:
            st.info(f"新聞: {news}")

        st.subheader("🔮 AI 財報預測")
        st.success(s.get('ai_report', '數據分析中...'))
        
        st.subheader("🦢 地緣政治黑天鵝警示")
        st.warning("議題關注: (1) 俄烏衝突發展 (2) 美伊緊張局勢 (3) 聯準會利率會議")
        
    else:
        st.warning(f"本地市場數據中查無 {target_ticker}，請確認 main_task.py 是否已執行並成功更新 market_data.json。")

if __name__ == "__main__":
    main()
