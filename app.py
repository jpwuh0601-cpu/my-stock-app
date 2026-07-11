# ... existing code ...
    }
    return data, "智慧程序化模擬引擎 (安全防當護航模式)", ticker

# --- 新增：使用快取機制優化數據讀取速度 ---
@st.cache_data(ttl=600, show_spinner=False)
def get_cached_data(ticker_input):
    return fetch_realtime_stock_quote(ticker_input)
# --------------------------------------

def render_html_table(data_list, title):
# ... existing code ...
st.sidebar.markdown("## 🔍 實時自主查詢系統")
ticker_input = st.sidebar.text_input("輸入您想查詢的股票代號", "3294")
query_btn = st.sidebar.button("立即實時查詢")

# --- 修改：改用快取函式 ---
with st.spinner("正在讀取金融數據..."):
    data, source, final_ticker = get_cached_data(ticker_input)
# -------------------------

# 系統連線狀態顯示
status_color = "#E53E3E" if "防當" in source or "模擬" in source else "#319795"
# ... existing code ...
```

### 修正重點：
1.  **引入 `st.cache_data`**：將 `fetch_realtime_stock_quote` 的呼叫結果快取 10 分鐘 (600秒)，這樣即便頁面自動重載，也不會重複觸發 API 連線，解決 Spinner 卡死的問題。
2.  **`show_spinner=False`**：在快取函式中設定為 `False`，避免預設 Spinner 與我們自訂的 `st.spinner` 衝突。
3.  **UI 體驗優化**：包覆在 `st.spinner("正在讀取金融數據...")` 內，給使用者更明確的載入提示，而不是系統底層不明確的等待。

請將上述修改更新至您的 `app.py`，卡頓現象應該會立即改善。
