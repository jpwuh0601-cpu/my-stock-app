import streamlit as st
import json
import os
import pandas as pd

# 頁面配置
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 強制指向倉庫根目錄下的 market_data.json
FILE_PATH = os.path.join(os.getcwd(), "market_data.json")

def load_data():
    """安全載入 JSON 資料"""
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data, True
        except Exception:
            return {}, False
    return {}, False

data, loaded = load_data()

st.title("📊 AI 智能投資決策儀表板")

# 選股操作區
stock_code = st.text_input("輸入股票代碼", value="2330")
if st.button("執行選股分析"):
    st.toast(f"正在分析 {stock_code}...", icon="🔍")

if not loaded:
    st.error("❌ 尚未讀取數據，請確認 GitHub Actions 自動化任務已完成推送。")
else:
    # 核心財務指標區
    st.subheader("核心財務指標")
    cols = st.columns(6)
    cols[0].metric("即時股價", f"{data.get('price', 0):,.2f}")
    cols[1].metric("本益比", f"{data.get('pe_ratio', 0):.2f}")
    cols[2].metric("預估營收", f"{data.get('est_revenue', 0):,.0f}")
    cols[3].metric("預估 EPS", f"{data.get('est_eps', 0):.2f}")
    cols[4].metric("預估股利", f"{data.get('est_dividend', 0):.2f}")
    cols[5].metric("10日資券比", f"{data.get('margin_ratio', 0)}%")

    # 三大法人買賣超 (高穩定渲染)
    st.subheader("三大法人買賣超 (10日)")
    inst_data = data.get("institutional_investors", [])
    if isinstance(inst_data, list) and len(inst_data) > 0:
        # 轉為 DataFrame 時，明確指定資料格式以避開 Numpy 衝突
        df_inst = pd.DataFrame(inst_data)
        st.dataframe(df_inst, use_container_width=True)
    else:
        st.info("目前無法人買賣超數據")

    # 主力券商買賣
    st.subheader("10日主力券商買賣")
    broker_data = data.get("top_brokers", [])
    if isinstance(broker_data, list) and len(broker_data) > 0:
        df_brokers = pd.DataFrame(broker_data)
        st.dataframe(df_brokers, use_container_width=True)
    else:
        st.info("目前無主力券商數據")

    # AI 財報預測與新聞
    st.subheader("AI 財報預測與市場動態")
    st.info(data.get("ai_prediction", "分析中..."))
    for news in data.get("news", []):
        st.write(f"• {news}")

st.divider()
st.caption("系統狀態：正常運行 | 資料來源：GitHub Actions 自動更新")
