import streamlit as st
import pandas as pd
import json
import os

def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def main():
    st.set_page_config(layout="wide", page_title="AI 智能金融終端")
    
    data = load_data()
    
    # 核心數據提取 (設定預設值)
    price = float(data.get("price", 0))
    change = float(data.get("change", 0))
    bvps = float(data.get("bvps", 0))
    margin_ratio = float(data.get("margin_ratio", 0))
    eps = float(data.get("eps_forecast", 0))
    
    # 標題
    st.title("📊 AI 智能金融終端")
    
    # 1. 核心指標 (漲紅跌綠)
    st.subheader("核心財務指標")
    cols = st.columns(4)
    
    # 處理漲跌顯示：如果 change 為 0，則不顯示 delta，避免 API 錯誤
    delta_str = f"{change:+.2f}" if change != 0 else None
    
    cols[0].metric("即時股價", f"{price:,.2f}", delta=delta_str)
    cols[1].metric("每股淨值", f"{bvps:.2f}")
    cols[2].metric("10日資券比", f"{margin_ratio:.2f}%")
    cols[3].metric("預估 EPS", f"{eps:.2f}")
        
    st.divider()

    # 2. 籌碼分析
    st.subheader("三大法人與籌碼數據")
    df_inst = pd.DataFrame(data.get("institutional_investors", []))
    if not df_inst.empty:
        st.dataframe(df_inst, use_container_width=True)
    else:
        st.write("目前無法人數據，請確認 worker.py 執行狀態。")

    # 3. AI 分析
    st.subheader("AI 市場趨勢分析")
    st.info(data.get("ai_prediction", "AI 正在分析數據中..."))

if __name__ == "__main__":
    main()
