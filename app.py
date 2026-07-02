import streamlit as st
import pandas as pd
import json
import os

# 設定頁面配置
st.set_page_config(layout="wide", page_title="AI 智能金融終端")

def load_data():
    """使用絕對路徑載入數據"""
    # 獲取 app.py 所在的目錄路徑
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "market_data.json")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"數據檔載入失敗: {e}")
            return {}
    else:
        st.error(f"找不到數據檔: {file_path}，請確認 worker.py 是否已產生檔案")
        return {}

def main():
    data = load_data()
    st.title("📈 AI 智能金融監控終端")
    
    if not data:
        st.warning("目前無數據顯示。")
        return

    # 1. 核心財務指標 (依照您的順序)
    st.subheader("核心財務指標")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("即時股價", f"{data.get('price', 0):,.2f}", delta=f"{data.get('change', 0):+.2f}")
    c2.metric("每股淨值", f"{data.get('bvps', 0):.2f}")
    c3.metric("本益比", f"{data.get('pe_ratio', 0):.2f}")
    c4.metric("10日資券比", f"{data.get('margin_ratio', 0):.2f}%")
    c5.metric("預估 EPS", f"{data.get('eps_forecast', 0):.2f}")

    # 2. 財報報表與分析
    tab1, tab2 = st.tabs(["財務報表與預測", "籌碼與主力分析"])
    
    with tab1:
        st.subheader("今年與去年每季財務報表")
        st.table(pd.DataFrame(data.get("financials", {})))
        st.subheader("AI 財報預測")
        st.success(data.get("ai_prediction", "分析中..."))

    with tab2:
        st.subheader("三大法人 10日買賣超")
        st.dataframe(pd.DataFrame(data.get("institutional_investors", [])), use_container_width=True)
        st.subheader("10日主力券商動向")
        st.dataframe(pd.DataFrame(data.get("top_brokers", [])), use_container_width=True)

    # 3. 新聞與監控
    st.divider()
    st.subheader("即時新聞解讀")
    st.info(data.get("news", "無即時新聞"))

if __name__ == "__main__":
    main()
