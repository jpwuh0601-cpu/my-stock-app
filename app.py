import streamlit as st
import json
import os
import pandas as pd

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 資料檢查函式 (自動化回測/驗證)
def verify_data(data):
    required_keys = ["price", "bvps", "financials", "institutional_investors", "margin_ratio"]
    missing = [key for key in required_keys if key not in data]
    return missing

# UI 樣式：紅色買超/綠色賣超
def color_negative_red(val):
    color = 'red' if val > 0 else 'green'
    return f'color: {color}'

st.title("📊 AI 智能投資決策儀表板")

# 讀取檔案
json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_data.json")
data = {}
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

# 股票搜尋側邊欄
stock_code = st.sidebar.text_input("輸入台股代碼 (例如: 1301)")
if st.sidebar.button("開始搜尋"):
    if not data:
        st.error("系統尚未載入數據，請檢查 GitHub Actions 狀態。")
    else:
        # 資料驗證
        missing_keys = verify_data(data)
        if missing_keys:
            st.warning(f"警告：部分資料欄位缺失: {', '.join(missing_keys)}")
        else:
            st.success("數據源驗證通過，載入完成。")

        # 1-3. 關鍵指標
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("即時股價", f"{data.get('price', 'N/A')}")
        c2.metric("每股淨值", f"{data.get('bvps', 'N/A')}")
        c3.metric("預估營收", f"{data.get('est_revenue', 'N/A')}")
        c4.metric("預估 EPS", f"{data.get('est_eps', 'N/A')}")
        c5.metric("預估股利", f"{data.get('est_dividend', 'N/A')}")

        st.divider()

        # 4. 每季財報
        st.subheader("📝 今年與去年每季財報")
        financials = data.get("financials", {})
        df_fin = pd.DataFrame(financials).T
        st.dataframe(df_fin, use_container_width=True)

        # 5. 三大法人買賣超 (10日)
        st.subheader("📈 三大法人買賣超 (10日)")
        inst_data = data.get("institutional_investors", [])
        if inst_data:
            df_inst = pd.DataFrame(inst_data)
            st.dataframe(df_inst.style.map(color_negative_red, subset=['買賣超']), use_container_width=True)
        else:
            st.info("暫無法人數據")

        # 6. 10日資券比
        st.subheader("📊 10日資券比")
        st.metric("當前資券比", f"{data.get('margin_ratio', 'N/A')}%")

        # 7. 主力券商買賣 (10日)
        st.subheader("🏢 主力券商買賣 (10日)")
        brokers = data.get("top_brokers", [])
        st.dataframe(pd.DataFrame(brokers), use_container_width=True)

        # 8. 即時新聞
        st.subheader("📰 即時新聞")
        for news in data.get("news", ["無最新新聞"]):
            st.write(f"- {news}")

        # 9. AI 財報預測 (調整至新聞後)
        st.subheader("🤖 AI 財報預測")
        st.info(data.get("ai_prediction", "暫無預測資料"))

else:
    st.info("請輸入代碼後按下搜尋。")
