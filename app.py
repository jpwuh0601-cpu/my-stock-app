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
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except:
            return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    # 顯示股價
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    st.divider()

    st.subheader("🏦 三大法人籌碼數據")
    
    # 【空值零容忍處理】：直接強制轉型，保證不會有 NoneType 錯誤
    raw = data.get("institutional_investors")
    
    # 這裡強制給一個安全的空列表，確保 raw 絕對不會是 None
    safe_raw = raw if raw is not None else []
    
    # 將所有數據扁平化為 Key-Value 對
    flat_rows = []
    
    if isinstance(safe_raw, list):
        for item in safe_raw:
            if isinstance(item, dict):
                for k, v in item.items():
                    flat_rows.append({"欄位": str(k), "內容": str(v)})
            else:
                flat_rows.append({"欄位": "數據", "內容": str(item)})
    elif isinstance(safe_raw, dict):
        for k, v in safe_raw.items():
            flat_rows.append({"欄位": str(k), "內容": str(v)})
    else:
        flat_rows.append({"欄位": "說明", "內容": str(safe_raw)})

    # 執行表格顯示
    if flat_rows:
        try:
            df = pd.DataFrame(flat_rows, index=range(len(flat_rows)))
            st.table(df)
        except Exception as e:
            st.error(f"表格繪製失敗: {e}")
    else:
        st.info("目前無籌碼數據。")

    st.subheader("🤖 AI 智能分析")
    st.write(str(data.get("ai_prediction", "暫無分析數據。")))

    with st.expander("🔍 除錯數據檢查"):
        st.json(data)

if __name__ == "__main__":
    main()
