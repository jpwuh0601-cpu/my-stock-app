import streamlit as st
import subprocess
import os
import time

st.set_page_config(page_title="即時金融查詢器", layout="wide")
st.title("📊 即時金融查詢器")

# 輸入區塊
ticker_input = st.text_input("輸入股票代號 (例如: 2330.TW)", placeholder="2330.TW")
query_btn = st.button("立即分析")

# 查詢邏輯
if query_btn and ticker_input:
    with st.spinner(f"正在分析 {ticker_input}..."):
        # 移除舊的結果檔案
        result_file = "analysis_result.txt"
        if os.path.exists(result_file):
            os.remove(result_file)
            
        # 執行 main_task.py 進行分析
        try:
            # 呼叫 main_task.py 並傳入 ticker 參數
            subprocess.run(["python", "main_task.py", "--ticker", ticker_input], check=True)
            
            # 等待檔案生成
            time.sleep(1)
            
            # 讀取分析結果
            if os.path.exists(result_file):
                with open(result_file, "r", encoding="utf-8") as f:
                    analysis_content = f.read()
                
                st.subheader("🤖 AI 分析結果")
                st.info(analysis_content)
            else:
                st.error("分析過程發生錯誤，未產生結果檔案。")
                
        except Exception as e:
            st.error(f"分析程序執行失敗: {e}")

st.markdown("---")
st.caption("輸入代號後點擊「立即分析」，系統將即時呼叫後端模組進行 AI 財報解讀。")
