import streamlit as st
import json
import os

st.set_page_config(page_title="AI 投資秘書除錯", layout="wide")
st.title("📈 AI 投資秘書儀表板 (除錯模式)")

# 1. 偵測目前工作目錄
cwd = os.getcwd()
st.write(f"目前 Streamlit 運行的路徑: `{cwd}`")

# 2. 搜尋該目錄下所有檔案
all_files = os.listdir(cwd)
st.write(f"當前目錄下的檔案: `{all_files}`")

file_path = os.path.join(cwd, "market_data.json")

if os.path.exists(file_path):
    st.success("成功找到 market_data.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            st.write("檔案內容預覽:", data) # 直接把內容印出來檢查
            
            # 嘗試顯示第一個代號
            if isinstance(data, dict) and len(data) > 0:
                first_key = list(data.keys())[0]
                st.write(f"成功解析到個股: {first_key}")
            else:
                st.warning("檔案內容為空或是格式不是字典")
    except Exception as e:
        st.error(f"解析 JSON 失敗: {e}")
else:
    st.error(f"在 {cwd} 找不到 market_data.json")
