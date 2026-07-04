import streamlit as st
import json
import os

st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

# 強制讀取本地 JSON，不直接呼叫外部 API
@st.cache_data(ttl=60)
def load_data():
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"數據讀取錯誤: {e}")
    return {}

data = load_data()

st.subheader("🔍 選擇監控標的")

if not data:
    st.error("目前沒有數據。請確認 GitHub Actions 是否已順利執行並生成 market_data.json。")
else:
    # 改用選單，徹底排除手動輸入可能導致的 API 頻繁請求
    ticker_options = list(data.keys())
    selected_ticker = st.selectbox("請從清單中選擇標的:", ticker_options)

    # 讀取對應數據
    m = data.get(selected_ticker, {})
    
    # 呈現區塊
    c1, c2, c3 = st.columns(3)
    c1.metric("即時股價", f"{m.get('price', 0):.2f}")
    c2.metric("本益比", f"{m.get('pe', 0):.2f}")
    c3.metric("EPS", f"{m.get('eps', 0):.2f}")
    
    st.info(f"🤖 AI 分析: {m.get('ai_prediction', '數據初始化中...')}")
    st.warning(f"當前風險狀態: {m.get('black_swan', '安全')}")

st.markdown("---")
st.markdown("""
### 如何新增標的？
為了保證系統穩定（避免 API 被封鎖）：
1. 編輯專案中的 `tickers.txt`。
2. 在新的一行輸入您的標的（如：`6456.TW`）。
3. 提交變更到 GitHub。
4. 前往 **Actions** 頁面，點擊 **Run workflow**。
5. 等待綠色勾勾後，重新整理本頁，新股票就會自動出現。
""")
