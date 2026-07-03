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
    
    raw = data.get("institutional_investors")
    
    # 【徹底平坦化】：將所有資料強制轉為適合顯示的「列與值」二維結構
    rows = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                # 將每個字典變成 Key: Value 的一列
                for k, v in item.items():
                    rows.append({"項目": str(k), "數值": str(v)})
            else:
                rows.append({"項目": "說明", "數值": str(item)})
    elif isinstance(raw, dict):
        for k, v in raw.items():
            rows.append({"項目": str(k), "數值": str(v)})
    elif raw is not None:
        rows.append({"項目": "數據", "數值": str(raw)})

    # 表格顯示
    if rows:
        try:
            # 建立 DataFrame，明確指定資料來源為 rows
            df = pd.DataFrame(rows)
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
