import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    st.divider()

    st.subheader("🏦 三大法人籌碼數據")
    
    # 獲取原始數據
    raw = data.get("institutional_investors")
    
    # 進行完全的空值與型別檢查，確保不會拋出 NoneType 錯誤
    try:
        if raw is None:
            # 若為 None，直接顯示資訊，不觸發 DataFrame 轉換
            st.info("目前無籌碼數據。")
        elif isinstance(raw, list):
            # 若為列表，將內容全轉為字串字典
            processed = [{"欄位": str(i), "內容": str(item)} for i, item in enumerate(raw)]
            st.table(pd.DataFrame(processed))
        elif isinstance(raw, dict):
            # 若為字典，直接轉為鍵值對表格
            processed = [{"欄位": str(k), "內容": str(v)} for k, v in raw.items()]
            st.table(pd.DataFrame(processed))
        else:
            # 若為其他型別，直接顯示
            st.write(str(raw))
    except Exception as e:
        st.error(f"表格格式解析失敗: {e}")
        st.write("原始資料:", raw)

    st.subheader("🤖 AI 智能分析")
    st.write(str(data.get("ai_prediction", "暫無分析數據。")))

    with st.expander("🔍 除錯數據檢查"):
        st.json(data)

if __name__ == "__main__":
    main()
