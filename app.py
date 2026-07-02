import streamlit as st
import json
import os
import pandas as pd

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 設定檔案路徑
FILE_PATH = "market_data.json"

def load_data():
    """安全地載入 JSON 資料"""
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f), True
        except Exception as e:
            return {"error": str(e)}, False
    return {"error": "檔案不存在"}, False

# 載入資料
data, loaded = load_data()

st.title("📊 AI 智能投資決策儀表板")

# 選股操作區
with st.expander("🔍 股票篩選與操作"):
    stock_code = st.text_input("輸入股票代碼", "2330")
    if st.button("執行選股分析"):
        st.write(f"正在分析 {stock_code}...")

if not loaded:
    st.error(f"❌ 無法讀取資料: {data.get('error')}")
else:
    # 核心財務指標 (加入防錯 .get)
    st.subheader("核心財務指標")
    cols = st.columns(6)
    cols[0].metric("即時股價", f"{data.get('price', 0):,.2f}")
    cols[1].metric("每股淨值", f"{data.get('bvps', 0):,.2f}")
    cols[2].metric("預估營收", f"{data.get('est_revenue', 0):,.0f}")
    cols[3].metric("預估 EPS", f"{data.get('est_eps', 0):.2f}")
    cols[4].metric("預估股利", f"{data.get('est_dividend', 0):.2f}")
    cols[5].metric("10日資券比", f"{data.get('margin_ratio', 0)}%")

    # 今去年每季報表
    st.subheader("今年與去年每季報表")
    if "financials" in data and data["financials"]:
        st.dataframe(pd.DataFrame(data["financials"]).T, use_container_width=True)
    else:
        st.write("暫無財報數據")

    # 三大法人買賣超 (移除自營商邏輯)
    st.subheader("三大法人買賣超 (10日)")
    if "institutional_investors" in data and data["institutional_investors"]:
        df_inst = pd.DataFrame(data["institutional_investors"])
        st.dataframe(df_inst, use_container_width=True)
    else:
        st.write("暫無法人買賣數據")

    # 主力券商
    st.subheader("10日主力券商買賣")
    if "top_brokers" in data and data["top_brokers"]:
        st.dataframe(pd.DataFrame(data["top_brokers"]), use_container_width=True)
    else:
        st.write("暫無主力券商數據")

    # 新聞與預測
    st.subheader("即時新聞")
    for news in data.get("news", []):
        st.write(f"• {news}")

    st.subheader("AI 財報預測")
    st.info(data.get("ai_prediction", "分析中..."))

# 系統狀態
st.divider()
st.caption("系統狀態：正常運行")
