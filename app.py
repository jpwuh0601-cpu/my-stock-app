import streamlit as st
import json
import os
import pandas as pd

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

# 強制絕對路徑讀取 JSON
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "market_data.json")

def load_data():
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"檔案讀取失敗: {e}")
    return {}

def validate_data(data):
    """資料完整性自動檢核"""
    required_keys = ['price', 'bvps', 'financials']
    for key in required_keys:
        if key not in data:
            return False, f"缺少欄位: {key}"
    return True, "數據檢查通過"

def color_buy_sell(val):
    """買賣超顏色標示: 買(紅)>0, 賣(綠)<0"""
    if isinstance(val, (int, float)):
        return 'color: red' if val > 0 else 'color: green'
    return ''

data = load_data()
is_valid, msg = validate_data(data)

# 頂部狀態列
if is_valid:
    st.success(f"✅ {msg}")
else:
    st.warning(f"⚠️ 資料來源檢核: {msg}")

# 搜尋邏輯
stock_code = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")

if st.sidebar.button("開始搜尋") or stock_code:
    if data:
        # 1 & 2. 即時股價與每股淨額
        col1, col2 = st.columns(2)
        col1.metric("即時股價", f"{data.get('price', 0)}")
        col2.metric("每股淨值 (BVPS)", f"{data.get('bvps', 0)}")
        
        st.divider()

        # 4. 今年與去年每季財報
        st.subheader("📊 財務報表 (近兩年)")
        financials = data.get("financials", {})
        if financials:
            st.dataframe(pd.DataFrame.from_dict(financials, orient='index'), use_container_width=True)
        else:
            st.write("暫無財報數據")

        # 5. 三大法人買賣超 (10日)
        st.subheader("👥 三大法人買賣超 (近10日)")
        investors = data.get("institutional_investors", [])
        if investors:
            df_inv = pd.DataFrame(investors)
            st.dataframe(df_inv.style.map(color_buy_sell, subset=['買賣超']), use_container_width=True)
        else:
            st.write("暫無法人買賣數據")

        # 6. 10日資券比與主力券商
        st.subheader("📈 10日資券比與主力券商")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("10日資券比", f"{data.get('margin_ratio', 'N/A')}%")
        
        brokers = data.get("top_brokers", [])
        if brokers:
            st.table(pd.DataFrame(brokers))
        else:
            st.write("暫無主力券商數據")

        st.divider()

        # 顯示新聞
        st.subheader("📰 即時新聞")
        for news in data.get("news", ["暫無新聞"]):
            st.write(f"- {news}")

        # 7. AI 財報預測 (在新聞後)
        st.subheader("🤖 AI 財報分析與預測")
        st.info(data.get("ai_prediction", "暫無預測"))

        # 預估今年營收、EPS 與股利
        st.subheader("🔮 今年預估績效")
        est_col1, est_col2, est_col3 = st.columns(3)
        est_col1.metric("預估今年營收", data.get("est_revenue", "N/A"))
        est_col2.metric("預估 EPS", data.get("est_eps", "N/A"))
        est_col3.metric("預估股利", data.get("est_dividend", "N/A"))

    else:
        st.error("找不到市場數據檔案。")
else:
    st.info("請輸入代碼開始分析。")
```

### 接下來的行動清單：

1.  **更新 `app.py`**：將上述程式碼更新至您的 `app.py`。
2.  **升級 `worker.py`**：因為新版儀表板加入了 `est_revenue` (預估營收), `est_eps`, `est_dividend` (股利) 等欄位，您現在必須去修改 `worker.py`，在爬蟲或分析完畢後，確保 `json` 的寫入格式包含這些新欄位。
3.  **重新執行**：推送程式碼後，您的 GitHub Actions 會自動執行，並更新 `market_data.json`。屆時儀表板就會自動顯示完整數據，且會顯示「資料檢查通過」的綠色狀態條。

此佈局已根據您在 `image_0a1b94.png` 中顯示的環境配置，將版面調整為符合您要求的邏輯順序。
