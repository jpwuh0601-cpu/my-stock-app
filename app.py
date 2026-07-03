import streamlit as st
import json
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os

# 設定頁面布局
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """載入數據檔，若無則回傳空字典"""
    if not os.path.exists("market_data.json"):
        return {}
    with open("market_data.json", "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    if not data:
        st.warning("數據載入中或格式異常，請等待自動化排程更新。")
        return

    # 側邊欄選擇器
    tickers = [t for t in data.keys() if t != "last_updated"]
    selected = st.sidebar.selectbox("請選擇股票代號", tickers)
    
    # 定義 4 個頁籤
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 即時股價與財報", 
        "🏦 法人與資券籌碼", 
        "🤖 AI 分析與新聞", 
        "🛠 自動回測檢核"
    ])
    
    info = data.get(selected, {})
    
    # 頁籤 1：即時股價、EPS、每股淨額 (BVPS)、本益比
    with tab1:
        st.subheader(f"{selected} 監控數據")
        price = info.get("price", 0)
        
        # 顯示即時股價
        st.metric("即時股價", f"{price:,.2f}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("EPS", info.get("eps", "N/A"))
        col2.metric("每股淨值 (BVPS)", info.get("bvps", "N/A"))
        col3.metric("本益比 (PE)", info.get("pe", "N/A"))

    # 頁籤 2：三大法人與 10 日資券比
    with tab2:
        st.subheader("籌碼面數據")
        st.info("此區塊將整合三大法人 10 日買賣超與資券比數據 (需在 worker.py 加入對應爬蟲)")

    # 頁籤 3：AI 財報預測與新聞解讀
    with tab3:
        st.subheader("AI 財報預測與新聞解讀")
        st.write(info.get("ai_prediction", "暫無 AI 分析結果"))

    # 頁籤 4：自動回測系統檢核
    with tab4:
        st.subheader("自動回測系統檢核狀態")
        last_updated_str = data.get("last_updated", "2000-01-01 00:00:00")
        
        try:
            last_updated = datetime.strptime(last_updated_str, "%Y-%m-%d %H:%M:%S")
            if datetime.now() - last_updated > timedelta(hours=24):
                st.error(f"⚠️ 數據來源已過期！最後更新時間: {last_updated_str}")
            else:
                st.success(f"✅ 數據更新正常！最後更新時間: {last_updated_str}")
        except:
            st.error("時間戳記格式錯誤，請檢查 worker.py 寫入格式。")

if __name__ == "__main__":
    main()
