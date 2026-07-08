import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

def load_market_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return None

ticker_input = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")

if st.sidebar.button("查詢分析數據"):
    data = load_market_data()
    
    if data and ticker_input in data:
        stock_info = data[ticker_input]
        
        # 1. 股價顯示
        price = stock_info.get('price', 0)
        st.metric("即時股價", f"{price}")
        
        # 2. 深度清理表格數據 (關鍵修正！)
        if "institutional_data" in stock_info and isinstance(stock_info["institutional_data"], list):
            inst_df = pd.DataFrame(stock_info["institutional_data"])
            
            # 強制轉換所有數據為字串，避免 Pandas 渲染出錯
            st.markdown("### 4. 三大法人買賣超")
            st.table(inst_df.astype(str))
        else:
            st.warning("目前無法人數據資訊")
            
        # 3. AI 分析建議 (使用 st.write 替代 st.markdown 防止格式錯誤)
        st.markdown("### AI 智慧分析")
        st.write(stock_info.get("ai_prediction", "尚無 AI 分析內容"))
        
    else:
        st.error(f"⚠️ 找不到 {ticker_input} 的數據，請確認 market_data.json 結構是否正確。")
