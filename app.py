import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def safe_float(value):
    """安全地將任何值轉為浮點數，若失敗則返回 0.0"""
    try:
        return float(str(value).replace(',', '').replace('$', ''))
    except:
        return 0.0

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    # 核心指標：強制安全處理
    st.metric("即時股價", f"{safe_float(data.get('price')):,.2f}")
    
    st.divider()

    st.subheader("🏦 三大法人與籌碼數據")
    raw = data.get("institutional_investors")

    try:
        if raw:
            # 確保資料為列表
            data_list = raw if isinstance(raw, list) else [raw]
            
            # 使用 Pandas 讀取時，不要強制轉字串，讓 Pandas 自動判斷
            df = pd.DataFrame(data_list)
            
            # 顯示表格，並隱藏索引
            st.table(df)
        else:
            st.info("目前無籌碼數據。")
    except Exception as e:
        st.error(f"表格格式異常: {e}")

    st.subheader("🤖 AI 智能分析")
    st.write(str(data.get("ai_prediction", "暫無分析數據。")))

    with st.expander("🔍 除錯數據"):
        st.json(data)

if __name__ == "__main__":
    main()
