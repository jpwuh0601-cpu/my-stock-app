import streamlit as st
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控診斷終端")

def load_data():
    # 強制檢查檔案是否存在
    if not os.path.exists("market_data.json"):
        return {"error": "找不到 market_data.json 檔案"}
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": f"JSON 解析失敗: {str(e)}"}

def main():
    data = load_data()
    st.title("📈 診斷模式：AI 金融儀表板")
    
    # 顯示錯誤
    if "error" in data:
        st.error(data["error"])
        return

    st.subheader("📊 系統數據結構檢查")
    
    # 列出所有存在的鍵值
    all_keys = list(data.keys())
    st.write(f"目前偵測到的欄位: {all_keys}")
    
    # 針對目標欄位做防禦性檢查
    target = "institutional_investors"
    if target in data:
        st.success(f"成功偵測到 '{target}' 欄位！")
        st.json(data[target])
    else:
        st.warning(f"目前檔案中沒有 '{target}' 欄位。")
        st.write("這是常見的 GitHub Actions 同步問題，請檢查 worker.py 是否在雲端環境中有正確寫入。")

    st.divider()
    
    st.subheader("🔍 完整 JSON 原始數據")
    st.json(data)

if __name__ == "__main__":
    main()
