import streamlit as st
import pandas as pd
import numpy as np
from worker import fetch_stock_data

# 頁面配置 (使用寬版佈局)
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 側邊欄：輸入區
ticker_input = st.sidebar.text_input("輸入股票代號 (例如: 2330)", "2330")

# 設定快取：避免重複 API 呼叫導致卡死
@st.cache_data(ttl=600)
def get_stock_data_cached(ticker):
    return fetch_stock_data(ticker)

# 主邏輯區
if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取資料..."):
        try:
            data = get_stock_data_cached(ticker_input)
            
            if "error" in data:
                st.error(data["error"])
            else:
                # 1. 即時股價 (漲紅跌綠)
                st.subheader("1. 即時股價概況")
                price = data.get('price', 0)
                change = data.get('change', 0)
                color = "normal" if change >= 0 else "inverse"
                st.metric("即時股價", f"{price:.2f}", f"{change:.2f}", delta_color=color)
                
                # 2. 財務指標
                st.subheader("2. 財務數據")
                c1, c2, c3 = st.columns(3)
                c1.metric("每股淨值", f"{data.get('nav', 0):.2f}")
                c2.metric("本益比", f"{data.get('pe', 0):.2f}")
                c3.metric("EPS", f"{data.get('eps', 0):.2f}")

                # 使用 Tab 進行分區，這是防止頁面卡死的關鍵
                tab1, tab2, tab3, tab4 = st.tabs(["法人/券商籌碼", "財報預測", "技術指標", "黑天鵝與新聞"])

                with tab1:
                    st.subheader("法人與券商十日買賣超")
                    # 法人表格 (漲紅跌綠)
                    inst_df = pd.DataFrame(data.get("institutional_data"))
                    st.dataframe(inst_df.style.map(lambda x: 'color: red' if x > 0 else 'color: green', subset=['外資', '投信', '自營商']), use_container_width=True)

                with tab2:
                    st.subheader("AI 財報預測與營收預估")
                    st.write(data.get("ai_prediction", "分析中..."))
                    st.write(data.get("revenue_forecast", "預估數據讀取中..."))

                with tab3:
                    st.subheader("技術指標 (KD/MACD/RSI)")
                    tech_data = data.get("tech_indicators", {})
                    st.bar_chart(pd.DataFrame([tech_data]))
                    
                    st.subheader("股東持股分級")
                    sh_data = data.get("shareholder_structure", {})
                    # 繪製柱狀圖
                    st.bar_chart(pd.DataFrame([sh_data]))

                with tab4:
                    st.subheader("即時新聞與黑天鵝警示")
                    st.info(f"黑天鵝風險: {data.get('black_swan', '無明顯風險')}")
                    st.write("即時新聞:", data.get("news", "暫無新聞"))

        except Exception as e:
            st.error(f"系統錯誤: {str(e)}")
else:
    st.write("請輸入股票代號並點擊查詢。")
```

### 給您的下一步建議：
*   **如果仍有載入問題**：這是因為 Streamlit Cloud 環境限制，建議將 `worker.py` 中所有的 `yfinance` 獲取動作也加上 `@st.cache_data`，確保第一次獲取後，之後查詢瞬間顯示。
*   **關於回測功能**：您提到的「自動回測資料來源是否正確」涉及與 Yahoo Finance 的驗證機制，建議在 `worker.py` 中增加一個簡單的資料存在性檢查，如果 `info` 為空就回傳錯誤訊息，這樣您的儀表板就不會因為空資料而當機。

現在您可以重新嘗試，這個結構是最穩定的。
