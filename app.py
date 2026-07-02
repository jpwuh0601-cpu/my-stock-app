import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """讀取市場數據，強制確保回傳字典結構"""
    file_path = "market_data.json"
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    # 顯示股價
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    st.subheader("🏦 三大法人與籌碼數據")
    
    # 核心修正：使用防禦性處理邏輯
    raw = data.get("institutional_investors")
    
    # 強制將任何非列表型別的數據（含 None）轉為空列表
    if not isinstance(raw, list):
        if isinstance(raw, dict):
            proc_data = [raw]
        else:
            proc_data = []
    else:
        proc_data = raw

    # 呈現表格
    if proc_data:
        try:
            # 強制將所有資料轉為字串，避免型別不一致崩潰
            df = pd.DataFrame(proc_data)
            df = df.astype(str)
            st.table(df)
        except Exception as e:
            st.error(f"表格繪製異常: {e}")
            st.write("原始數據:", proc_data)
    else:
        st.info("目前無籌碼數據。")

    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析數據。"))

    # 除錯資訊
    with st.expander("🔍 除錯：查看完整數據"):
        st.json(data)

if __name__ == "__main__":
    main()
