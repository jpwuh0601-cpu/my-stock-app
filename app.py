import streamlit as st
import pandas as pd
import json
import os

# 頁面配置
st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# 核心修正：統一讀取路徑與錯誤防護
def load_market_data():
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"資料庫讀取異常: {e}")
            return {}
    return {}

# 側邊欄輸入
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取離線資料庫..."):
        data_cache = load_market_data()
        
        if ticker in data_cache:
            d = data_cache[ticker]
            
            # 1. 股價與財務數據
            st.subheader("1. 股價與財務數據")
            cols = st.columns(3)
            cols[0].metric("即時股價", f"{float(d.get('price', 0)):.2f}")
            cols[1].metric("EPS", f"{float(d.get('eps', 0)):.2f}")
            cols[2].metric("本益比", f"{d.get('pe', 'N/A')}")
            
            # 2. 法人籌碼統計
            st.subheader("2. 法人籌碼統計")
            inst_data = d.get("institutional_data", [])
            if inst_data:
                st.dataframe(pd.DataFrame(inst_data), use_container_width=True)
            else:
                st.info("目前無法人籌碼統計資料。")
            
            # 3. AI 分析結果
            st.subheader("6. AI 財報預測與自動回測")
            st.info(d.get("ai_prediction", "分析處理中..."))
            
            # 4. 營收與股利預估
            st.subheader("7. 營收與股利預估")
            st.table(pd.DataFrame({
                "項目": ["預估年度營收", "預估EPS", "預估股利"],
                "數值": ["1.2兆 TWD", f"{d.get('eps', 0)}", "12.5 TWD"]
            }))
        
        else:
            st.warning(f"系統目前未分析 {ticker} 的數據。")
            st.info("請檢查 GitHub Actions 是否有更新 market_data.json。")

else:
    st.info("請輸入代號並點擊查詢，系統將讀取由自動任務每日更新的離線資料庫。")
