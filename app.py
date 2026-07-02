import streamlit as st
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能監控診斷終端")

def load_data():
    # 強制使用絕對路徑
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if not os.path.exists(file_path):
        return {"error": f"找不到檔案於: {file_path}"}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": f"JSON 解析失敗: {str(e)}"}

def main():
    st.title("📈 AI 智能監控診斷終端")
    data = load_data()
    
    st.subheader("📊 檔案狀態")
    if "error" in data:
        st.error(data["error"])
    else:
        st.success("成功讀取到 market_data.json 檔案！")
        
        st.subheader("🔍 當前檔案內容結構")
        # 直接印出所有 keys，看看裡面到底有沒有 institutional_investors
        st.write("檔案中包含的 keys:", list(data.keys()))
        
        # 顯示完整數據，看看裡面到底是空的還是變成了別的名稱
        st.json(data)

if __name__ == "__main__":
    main()
