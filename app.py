import streamlit as st
import requests

# 頁面設定
st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# 【關鍵修正】使用您的 GitHub RAW 直連網址，繞過檔案路徑問題
RAW_URL = "https://raw.githubusercontent.com/jpwuh0601-cpu/my-stock-app/refs/heads/main/market_data.json"

@st.cache_data(ttl=600) # 快取數據 10 分鐘，避免頻繁請求
def load_data_from_github():
    """直接從 GitHub 網路位置抓取 JSON"""
    try:
        response = requests.get(RAW_URL, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"無法連接資料庫 (Status: {response.status_code})"}
    except Exception as e:
        return {"error": f"連線錯誤: {str(e)}"}

# 讀取資料
all_data = load_data_from_github()

# 側邊欄輸入
ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    if "error" in all_data:
        st.error(all_data["error"])
    elif ticker not in all_data:
        st.error(f"查無 '{ticker}' 的資料，請確認 GitHub Actions 是否已成功推送至 main 分支。")
    else:
        data = all_data[ticker]
        
        # 顯示指標數據
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", f"{data.get('price', 0):.2f}")
        col2.metric("每股淨額 (NAV)", f"{data.get('nav', 0):.2f}")
        col3.metric("本益比 (PE)", f"{data.get('pe', 0):.2f}")
        col4.metric("每股盈餘 (EPS)", f"{data.get('eps', 0):.2f}")
        
        # 顯示 AI 分析與籌碼
        st.subheader("6. AI 財報預測")
        st.info(data.get("ai_prediction", "AI 分析分析中..."))
        
        st.subheader("3. 三大法人買賣超 (10日)")
        st.write(data.get("institutional_data", "無資料"))

# 系統狀態顯示
st.sidebar.markdown("---")
st.sidebar.caption("系統運作狀態: 線上讀取中")
