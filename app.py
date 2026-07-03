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
    
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    st.divider()

    st.subheader("🏦 三大法人籌碼數據")
    
    raw = data.get("institutional_investors")
    
    # 【終極平坦化策略】：將任何數據結構轉為 List of {"欄位": K, "內容": V}
    # 這是 Pandas 解析最不會出錯的格式
    flat_rows = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                for k, v in item.items():
                    flat_rows.append({"欄位": str(k), "內容": str(v)})
            else:
                flat_rows.append({"欄位": "數據", "內容": str(item)})
    elif isinstance(raw, dict):
        for k, v in raw.items():
            flat_rows.append({"欄位": str(k), "內容": str(v)})
    elif raw is not None:
        flat_rows.append({"欄位": "數據", "內容": str(raw)})

    # 執行表格顯示
    if flat_rows:
        try:
            # 使用列表長度明確生成 index，解決 Scalar 值導致的 ValueError
            df = pd.DataFrame(flat_rows, index=range(len(flat_rows)))
            st.table(df)
        except Exception as e:
            st.error(f"表格格式解析異常: {e}")
            st.write("原始數據:", raw)
    else:
        st.info("目前無籌碼數據。")

    st.subheader("🤖 AI 智能分析")
    st.write(str(data.get("ai_prediction", "暫無分析數據。")))

    with st.expander("🔍 除錯數據檢查"):
        st.json(data)

if __name__ == "__main__":
    main()
