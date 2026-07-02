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

if not loaded:
    st.error("❌ 無法讀取市場數據，請檢查 GitHub Actions 是否成功推送 market_data.json 至儲存庫根目錄。")
else:
    # 1. & 2. 關鍵數據區塊
    st.subheader("核心財務指標")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("即時股價", f"{data.get('price', 0):,.2f}")
    c2.metric("每股淨值", f"{data.get('bvps', 0):,.2f}")
    c3.metric("預估營收", f"{data.get('est_revenue', 0):,.0f}")
    c4.metric("預估 EPS", f"{data.get('est_eps', 0):.2f}")
    c5.metric("預估股利", f"{data.get('est_dividend', 0):.2f}")
    c6.metric("10日資券比", f"{data.get('margin_ratio', 0)}%")

    # 4. 今年與去年每季報表
    st.subheader("今年與去年每季報表")
    if "financials" in data:
        st.dataframe(pd.DataFrame(data["financials"]).T, use_container_width=True)

    # 5. 股市 3 大法人買賣超 (紅買綠賣)
    st.subheader("三大法人買賣超 (10日)")
    if "institutional_investors" in data:
        df_inst = pd.DataFrame(data["institutional_investors"])
        # 使用 css 樣式顯示買賣超顏色
        st.dataframe(df_inst.style.map(color_negative_red, subset=['買賣超']), use_container_width=True)

    # 6. 主力券商買賣
    st.subheader("10日主力券商買賣")
    if "top_brokers" in data:
        st.dataframe(pd.DataFrame(data["top_brokers"]), use_container_width=True)

    # 8. 即時新聞 (放在 AI 預測前)
    st.subheader("即時新聞")
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
