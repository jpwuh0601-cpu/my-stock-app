import streamlit as st
import os
import json

# 強制設定頁面
st.set_page_config(layout="wide", page_title="系統診斷中心")

def main():
    st.title("🛠️ 系統診斷中心")
    
    st.markdown("### 環境狀態")
    st.write(f"**目前工作目錄 (CWD):** `{os.getcwd()}`")
    
    # 檢查 market_data.json 是否存在
    target_file = "market_data.json"
    if os.path.exists(target_file):
        st.success(f"✅ 找到檔案: {target_file}")
        st.write(f"**檔案完整路徑:** `{os.path.abspath(target_file)}`")
        
        try:
            with open(target_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                st.write("**檔案內容預覽:**")
                st.json(data)
        except Exception as e:
            st.error(f"❌ 檔案讀取/解析失敗: {e}")
    else:
        st.error(f"❌ 找不到檔案: {target_file}")
        st.info("請檢查 GitHub Actions 是否確實執行完畢且將檔案 Commit 到 main 分支。")

    st.markdown("### 環境變數檢查")
    st.write(f"**API KEY 狀態:** {'已檢測到' if 'OPENROUTER_API_KEY' in os.environ else '未檢測到 (可能需要重新部署)'}")

if __name__ == "__main__":
    main()
