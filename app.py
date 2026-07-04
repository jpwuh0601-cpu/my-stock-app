import streamlit as st
import json
import os

st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

# 1. 讀取數據，並確保結構正確
def load_data():
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

data = load_data()

# 2. 顯示資訊區塊
st.subheader("🔍 監控標的查詢")

if not data:
    st.error("數據尚未初始化。請確保 GitHub Actions 成功執行過。")
else:
    # 支援手動輸入或從清單選取
    all_tickers = list(data.keys())
    # 讓使用者可以輸入，並自動對應到清單
    selected_ticker = st.selectbox("請選擇或輸入標的:", all_tickers)
    
    # 顯示該標的的數據
    m = data.get(selected_ticker, {})
    
    # 使用 columns 呈現美觀數據
    c1, c2, c3 = st.columns(3)
    c1.metric("即時股價", f"{m.get('price', 0):.2f}")
    c2.metric("本益比", f"{m.get('pe', 0):.2f}")
    c3.metric("EPS", f"{m.get('eps', 0):.2f}")
    
    st.info(f"🤖 AI 分析: {m.get('ai_prediction', '正在等待資料更新...')}")
    st.warning(f"當前風險狀態: {m.get('black_swan', '安全')}")

st.markdown("---")
st.markdown("""
### 如何新增監控標的？
為了避免 Yahoo API 限制與轉圈問題，本系統已改為「後端預抓取」模式：
1. 開啟專案中的 `tickers.txt`。
2. 在裡面輸入您想要查詢的代號（例如：`1504.TW`）。
3. 儲存並提交到 GitHub。
4. 前往 **Actions** 頁面，點擊 **Run workflow**。
5. 等待綠色勾勾後，重新整理本網頁，您的新股票就會直接出現在清單中！
""")
