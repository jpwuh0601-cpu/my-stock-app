import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def main():
    data = load_data()
    if not data:
        st.warning("⚠️ 資料載入中...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    cols[1].metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    cols[2].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[3].metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    cols[4].metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    # 籌碼面：極嚴格檢查
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors")
    
    # 檢查是否為列表
    if isinstance(inst_data, list):
        valid_items = []
        for item in inst_data:
            # 必須確認 item 是字典才能進行下一步，避免 string indices error
            if isinstance(item, dict):
                valid_items.append(item)
        
        if valid_items:
            df = pd.DataFrame(valid_items)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("籌碼數據目前無有效內容。")
    else:
        st.info("籌碼數據格式錯誤，無法顯示表格。")

    st.subheader("AI 智能分析")
    st.write(data.get("ai_prediction", "暫無數據"))

if __name__ == "__main__":
    main()
