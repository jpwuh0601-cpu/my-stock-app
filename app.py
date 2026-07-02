import streamlit as st
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
    
    # 顯示股價
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    st.subheader("🏦 三大法人與籌碼數據")
    
    # 直接讀取，不做任何強制轉換，只做型別檢查
    raw = data.get("institutional_investors")
    
    # 使用 st.json 進行顯示，這是最安全的呈現方式，絕不會報 KeyError
    if raw:
        st.write("以下為籌碼原始數據：")
        st.json(raw)
    else:
        st.info("目前無籌碼數據，請檢查 JSON 來源檔案內容。")

    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析數據。"))

    with st.expander("🔍 除錯檢查：完整檔案內容"):
        st.json(data)

if __name__ == "__main__":
    main()
