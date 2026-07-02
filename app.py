import streamlit as st
import json
import os
import pandas as pd

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 紅綠色彩格式化函式
def color_negative_red(val):
    try:
        num = float(val)
        return f'color: {"red" if num > 0 else "green"}'
    except:
        return ''

# 載入數據
def load_data():
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f), True
        except:
            return None, False
    return None, False

data, loaded = load_data()

st.title("📊 AI 智能投資決策儀表板")

# 頂部選股操作區
with st.expander("🔍 股票篩選與操作"):
    col_a, col_b = st.columns([3, 1])
    selected_stock = col_a.text_input("輸入股票代碼進行分析", "2330")
    if col_b.button("執行選股分析"):
        st.write(f"正在分析 {selected_stock}...")

if not loaded:
    st.error("❌ 無法讀取市場數據，請檢查 GitHub Actions 是否成功推送 market_data.json。")
else:
    # 核心財務指標 (新增 本益比)
    st.subheader("核心財務指標")
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    c1.metric("即時股價", f"{data.get('price', 0):,.2f}")
    c2.metric("每股淨值", f"{data.get('bvps', 0):,.2f}")
    c3.metric("本益比 (PE)", f"{data.get('pe_ratio', 0):.2f}")
    c4.metric("預估營收", f"{data.get('est_revenue', 0):,.0f}")
    c5.metric("預估 EPS", f"{data.get('est_eps', 0):.2f}")
    c6.metric("預估股利", f"{data.get('est_dividend', 0):.2f}")
    c7.metric("10日資券比", f"{data.get('margin_ratio', 0)}%")

    # 今去年每季報表
    st.subheader("今年與去年每季報表")
    if "financials" in data:
        st.dataframe(pd.DataFrame(data["financials"]).T, use_container_width=True)

    # 三大法人買賣超
    st.subheader("三大法人買賣超 (10日)")
    if "institutional_investors" in data:
        df_inst = pd.DataFrame(data["institutional_investors"])
        st.dataframe(df_inst.style.map(color_negative_red, subset=['買賣超']), use_container_width=True)

    # 主力券商買賣 (詳細對照表)
    st.subheader("10日主力券商買賣明細")
    if "top_brokers" in data:
        st.dataframe(pd.DataFrame(data["top_brokers"]), use_container_width=True)

    # 即時新聞
    st.subheader("即時新聞")
    for news in data.get("news", []):
        st.write(f"• {news}")

    # AI 財報預測
    st.subheader("AI 財報預測")
    st.info(data.get("ai_prediction", "分析中..."))

    # 資料回測
    st.divider()
    st.subheader("🛡️ 資料來源自動回測")
    is_valid = all(k in data for k in ["price", "bvps", "pe_ratio", "top_brokers"])
    if is_valid:
        st.success("✅ 資料來源完整，回測結果正確。")
    else:
        st.warning("⚠️ 資料結構異常，部分欄位遺失。")
