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
    
    # 核心指標：增加對 KeyError 的防護 (使用 .get)
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    # 籌碼面：完全防禦邏輯
    st.subheader("🏦 三大法人與籌碼數據")
    
    # 使用 .get 獲取，若無該欄位則返回 None
    raw = data.get("institutional_investors")
    
    # 強制檢測
    if raw is None:
        st.info("⚠️ 目前尚未抓取到籌碼數據 (institutional_investors 欄位為空)。")
    else:
        try:
            # 確保它是列表結構
            data_list = raw if isinstance(raw, list) else [raw]
            df = pd.DataFrame(data_list)
            st.dataframe(df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"數據顯示異常: {e}")

    # AI 分析區塊
    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無 AI 分析結果。"))

    # 除錯：查看目前 JSON 到底有什麼內容
    with st.expander("🔍 除錯：查看完整 JSON 數據內容"):
        st.json(data)

if __name__ == "__main__":
    main()
