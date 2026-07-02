import streamlit as st
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {"error": str(e)}
    return {"error": "檔案不存在"}

def main():
    data = load_data()
    st.title("📈 AI 智能金融監控終端")
    
    # 顯示所有可用的鍵值，檢查欄位名稱
    st.subheader("系統狀態監控")
    st.write(f"目前讀取到的可用鍵值: {list(data.keys()) if isinstance(data, dict) else '資料格式異常'}")
    
    st.divider()

    # 直接顯示 JSON，不再預設任何欄位
    st.subheader("完整數據概覽")
    st.json(data)
    
    if "error" in data:
        st.error(f"錯誤訊息: {data['error']}")

if __name__ == "__main__":
    main()
