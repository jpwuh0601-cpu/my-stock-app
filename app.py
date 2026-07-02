import streamlit as st
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控診斷終端")

def load_data():
    """讀取市場數據，增加錯誤處理"""
    file_path = "market_data.json"
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def main():
    st.title("📈 AI 智能金融監控診斷終端")
    data = load_data()
    
    if data is None:
        st.error("找不到 market_data.json，請檢查 GitHub Actions 是否成功寫入檔案。")
        return

    # 顯示所有存在的鍵值 (這能幫我們找出為什麼 institutional_investors 不見了)
    available_keys = list(data.keys())
    st.subheader("📊 系統數據結構檢查")
    st.write(f"目前檔案中存在的欄位: {available_keys}")
    
    st.divider()

    # 如果有我們想要的欄位就顯示，沒有就提示
    target = "institutional_investors"
    if target in data:
        st.subheader("🏦 三大法人與籌碼數據")
        st.json(data[target])
    else:
        st.warning(f"目前數據中找不到 '{target}' 欄位。")
        st.info("請檢查 worker.py 是否在 cloud 環境中正確執行了數據抓取。")

    st.divider()
    
    with st.expander("🔍 查看完整原始 JSON"):
        st.json(data)

if __name__ == "__main__":
    main()
