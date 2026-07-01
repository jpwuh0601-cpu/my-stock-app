import streamlit as st
import json
import os
import pandas as pd

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

# 使用絕對路徑獲取檔案
def get_data_path():
    # 確保指向程式執行所在目錄下的檔案
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_data.json")

def load_data():
    json_path = get_data_path()
    
    # 除錯顯示路徑
    # st.sidebar.write(f"正在讀取: {json_path}") 
    
    if not os.path.exists(json_path):
        st.warning(f"⚠️ 找不到資料檔案: {json_path}。請確認 GitHub 檔案是否已正確同步。")
        return None
        
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"解析 JSON 失敗: {e}")
        return None

# 輔助函數
def safe_get(data, key, default="N/A"):
    if not data: return str(default)
    val = data.get(key, default)
    return str(val) if val is not None else str(default)

data = load_data()

# 搜尋區塊
stock_code = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")

if st.sidebar.button("開始搜尋"):
    if data:
        st.success(f"已成功載入 {stock_code} 的市場資料！")
        
        # 1 & 2. 關鍵數據
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", safe_get(data, "price"))
        col2.metric("每股淨值", safe_get(data, "bvps"))
        col3.metric("預估今年 EPS", safe_get(data, "est_eps"))
        col4.metric("預估今年營收", safe_get(data, "est_revenue"))

        # 3. 財報
        st.subheader("今年與去年每季財報")
        financials = data.get("financials", {})
        if financials:
            st.dataframe(pd.DataFrame.from_dict(financials, orient='index'), use_container_width=True)

        # 4. 法人買賣超
        st.subheader("三大法人買賣超 (10日)")
        investors = data.get("institutional_investors", [])
        if investors:
            st.dataframe(pd.DataFrame(investors), use_container_width=True)

        # 5. 資券比
        st.subheader("10日資券比與主力券商")
        st.metric("當前資券比", f"{safe_get(data, 'margin_ratio', '0')}%")

        # 6. 新聞與 AI 預測
        st.subheader("即時新聞")
        for news in data.get("news", ["暫無最新新聞"]):
            st.write(f"• {news}")
            
        st.subheader("AI 財報預測")
        st.info(data.get("ai_prediction", "AI 模型分析中..."))
        
    else:
        st.error("資料讀取失敗，請確認 market_data.json 是否已存在於倉庫根目錄。")
