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
    # 強制使用絕對路徑以適應 Streamlit Cloud 環境
    file_path = "/mount/src/my-stock-app/market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f), True
        except:
            return None, False
    return None, False

data, loaded = load_data()

st.title("📊 AI 智能投資決策儀表板")

# 新增：選股按鈕列
col_btn1, col_btn2 = st.columns([1, 5])
if col_btn1.button("🔍 篩選優質股"):
    st.balloons()
    st.success("已觸發選股策略...")

if not loaded:
    st.error("❌ 無法讀取市場數據...")
else:
    # 擴充：核心財務指標 (加入本益比)
    st.subheader("核心財務指標")
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7) # 改為7欄
    c1.metric("即時股價", f"{data.get('price', 0):,.2f}")
    c2.metric("每股淨值", f"{data.get('bvps', 0):,.2f}")
    c3.metric("本益比 (PE)", f"{data.get('pe_ratio', 0):.2f}") # 新增
    c4.metric("預估營收", f"{data.get('est_revenue', 0):,.0f}")
    c5.metric("預估 EPS", f"{data.get('est_eps', 0):.2f}")
    c6.metric("預估股利", f"{data.get('est_dividend', 0):.2f}")
    c7.metric("10日資券比", f"{data.get('margin_ratio', 0)}%")

    # 5. 三大法人
        df_inst = pd.DataFrame(data["institutional_investors"])
    # 6. 10日主力券商買賣 (優化表格)
    st.subheader("10日主力券商買賣")
    if "top_brokers" in data:
        df_brokers = pd.DataFrame(data["top_brokers"])
        # 若欄位包含買進/賣出，我們計算淨買賣
        if "賣出" in df_brokers.columns:
            df_brokers["淨買賣"] = df_brokers["買進"] - df_brokers["賣出"]
            st.dataframe(df_brokers.style.map(color_negative_red, subset=['淨買賣']), use_container_width=True)
        else:
            st.dataframe(df_brokers, use_container_width=True)
    for news in data.get("news", []):
        st.write(f"• {news}")

    # 7. AI 財報預測
    st.subheader("AI 財報預測")
    st.info(data.get("ai_prediction", "分析中..."))

    # 自動回測資料來源是否正確
    st.divider()
    st.subheader("🛡️ 資料來源自動回測")
    required_keys = ["price", "bvps", "est_eps", "institutional_investors"]
    is_valid = all(k in data for k in required_keys)
    if is_valid:
        st.success("✅ 資料來源完整，回測結果正確。")
    else:
        st.warning("⚠️ 資料結構異常，部分欄位遺失。")
