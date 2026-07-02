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
    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    st.subheader("🏦 三大法人與籌碼數據")
    raw = data.get("institutional_investors")

    # 【極限防禦】：我們直接印出到底讀到了什麼，並嘗試極簡化顯示
    st.write(f"資料型態: {type(raw)}")
    
    try:
        # 強制邏輯：如果不是 list，絕對不丟給 DataFrame
        if isinstance(raw, list):
            # 建立表格前確保每個 item 是 dict
            df_list = [item if isinstance(item, dict) else {"內容": str(item)} for item in raw]
            df = pd.DataFrame(df_list)
            st.table(df) # 使用 st.table 替代 st.dataframe 提高容錯率
        else:
            st.info("籌碼數據非列表格式，無法顯示表格。")
            st.write("原始資料內容:", raw)
    except Exception as e:
        st.error(f"表格顯示異常: {e}")

    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析數據。"))

if __name__ == "__main__":
    main()
