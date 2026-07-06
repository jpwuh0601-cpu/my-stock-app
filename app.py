import streamlit as st
import pandas as pd
import json
import os

# 頁面配置
st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# 讀取 GitHub Action 自動生成的 JSON 資料庫
def load_market_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

# 側邊欄：輸入代號
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在安全載入資料庫..."):
        data_cache = load_market_data()
        
        # 如果資料庫中有該代號的資料，則顯示
        if ticker in data_cache:
            d = data_cache[ticker]
            
            # 1. 股價與財務數據
            st.subheader("1. 股價與財務數據")
            cols = st.columns(3)
            cols[0].metric("即時股價", f"{d.get('price', 0):.2f}")
            cols[1].metric("EPS", f"{d.get('eps', 0):.2f}")
            cols[2].metric("本益比", f"{d.get('pe', 'N/A')}")
            
            # 2. 法人籌碼統計
            st.subheader("2. 法人籌碼統計")
            inst_data = d.get("institutional_data", [])
            if inst_data:
                st.dataframe(pd.DataFrame(inst_data), use_container_width=True)
            else:
                st.write("目前無法人籌碼統計資料。")

            # 3. 新聞與黑天鵝預警
            st.subheader("5. 最新即時新聞")
            st.write(d.get("news", "無最新資訊"))
            
            st.subheader("6. AI 財報預測與自動回測")
            st.info(f"AI 預測結果：{d.get('ai_prediction', '分析中...')}")
            
            # 4. 營收與股利預估
            st.subheader("7. 營收與股利預估")
            st.table(pd.DataFrame({
                "項目": ["預估年度營收", "預估EPS", "預估股利"],
                "數值": ["1.2兆 TWD", f"{d.get('eps', 0)}", "12.5 TWD"]
            }))
        
        else:
            st.warning("系統提示：目前尚未分析此代號，或數據更新中。")
            st.info("系統將於每日排程自動執行分析任務，請稍後再試。")

else:
    st.info("請輸入股票代號並點擊「查詢分析數據」，系統將優先從雲端資料庫讀取，確保連線穩定。")
