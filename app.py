import streamlit as st
import json
import os
import pandas as pd

# 頁面配置
st.set_page_config(page_title="AI 智能選股決策儀表板", layout="wide")

# 設定路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "market_data.json")

def load_data():
    if not os.path.exists(FILE_PATH) or os.path.getsize(FILE_PATH) == 0:
        return None
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def main():
    st.title("📊 AI 智能選股決策儀表板")
    
    # 1. 互動式選股區域
    st.sidebar.header("選股設定")
    stock_list = ["2330 台積電", "2317 鴻海", "2454 聯發科"] # 未來可從 JSON 動態讀取
    selected_stock = st.sidebar.selectbox("請選擇目標股票", stock_list)
    
    if st.sidebar.button("確認選股"):
        st.sidebar.success(f"已鎖定: {selected_stock}")
    
    # 載入資料
    data = load_data()
    if data is None:
        st.info("⚠️ 數據同步中，請稍候...")
        return

    # 2. 顯示核心指標
    st.subheader(f"當前標的: {selected_stock} 核心指標")
    cols = st.columns(4)
    cols[0].metric("最新股價", f"{float(data.get('price', 0)):,.2f}")
    cols[1].metric("融資券比", f"{data.get('margin_ratio', 0)}%")
    cols[2].metric("本益比", f"{float(data.get('pe_ratio', 0)):.1f}")
    cols[3].metric("淨值", f"{float(data.get('bvps', 0)):.1f}")

    # 3. 10日累計數據呈現
    st.divider()
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.subheader("三大法人 10日累計買賣超")
        # 假設資料結構包含 'institutional_10d'
        inst_data = data.get("institutional_10d", [{"機構": "外資", "10日累計": 5000}])
        st.dataframe(pd.DataFrame(inst_data), use_container_width=True)

    with col_r:
        st.subheader("主力券商 10日累計買賣")
        # 假設資料結構包含 'brokers_10d'
        broker_data = data.get("brokers_10d", [{"券商": "凱基", "10日累計": 12000}])
        st.dataframe(pd.DataFrame(broker_data), use_container_width=True)

    # 4. AI 分析
    st.subheader("AI 市場趨勢分析")
    st.success(data.get("ai_prediction", "分析準備中..."))

if __name__ == "__main__":
    main()
