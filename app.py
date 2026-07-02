import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="除錯儀表板", layout="wide")

st.title("🛠️ 除錯專用儀表板")

# 1. 強制讀取並驗證檔案
file_path = "market_data.json"

if not os.path.exists(file_path):
    st.error(f"錯誤：找不到檔案 {file_path}，目前的執行目錄是: {os.getcwd()}")
else:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            st.success("JSON 檔案讀取成功！")
            
            # 顯示原始資料結構，確認 Key 是否正確
            with st.expander("查看原始 JSON 資料"):
                st.json(data)
                
            # 2. 測試關鍵欄位 (依照您的需求檢測)
            required_keys = ["price", "bvps", "est_revenue", "est_eps", "institutional_investors"]
            
            st.subheader("欄位檢測結果")
            for key in required_keys:
                if key in data:
                    st.write(f"✅ 欄位 `{key}` 存在")
                else:
                    st.error(f"❌ 缺少必要欄位: `{key}`")

            # 3. 嘗試渲染表格 (這是最常導致白屏的部分)
            st.subheader("表格渲染測試")
            try:
                df_inst = pd.DataFrame(data.get("institutional_investors", []))
                st.dataframe(df_inst)
                st.write("✅ 表格渲染成功")
            except Exception as e:
                st.error(f"表格渲染失敗: {str(e)}")

    except json.JSONDecodeError:
        st.error("錯誤：JSON 格式損壞，請檢查 worker.py 產出的內容。")
    except Exception as e:
        st.error(f"發生未知錯誤: {str(e)}")

st.divider()
st.info("若此頁面顯示正常，請將原有的 app.py 邏輯逐步放回，若此頁面仍無法顯示，請告訴我顯示的錯誤內容。")
