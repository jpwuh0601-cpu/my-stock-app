import streamlit as st
import json
import os

st.set_page_config(page_title="Debug Mode", layout="wide")

st.title("系統狀態除錯頁面")

# 1. 檢查檔案是否存在
file_path = "market_data.json"
if not os.path.exists(file_path):
    st.error(f"錯誤: 找不到檔案 {file_path}！請確認 GitHub Actions 是否執行成功。")
else:
    st.success(f"檔案 {file_path} 存在。")
    
    # 2. 安全讀取模式
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                st.warning("檔案內容是空的！請檢查 `main_task.py` 的寫入邏輯。")
            else:
                data = json.loads(content)
                st.write("檔案讀取成功！資料概覽：")
                st.json(data)
                
                # 簡單的搜尋功能
                ticker = st.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
                if ticker in data:
                    st.write(f"找到 {ticker} 的資料:", data[ticker])
                else:
                    st.info(f"檔案內無 {ticker} 的紀錄。")
    except json.JSONDecodeError as e:
        st.error(f"JSON 格式錯誤！請檢查檔案是否損壞。錯誤詳情：{e}")
        st.text("原始檔案內容：")
        st.code(content[:500]) # 顯示前500字元以便除錯
    except Exception as e:
        st.error(f"發生未預期的錯誤: {e}")

st.write("---")
st.write("若此頁面能正常顯示，代表環境已恢復。請檢查上述顯示的 JSON 內容是否為您預期的結構。")
