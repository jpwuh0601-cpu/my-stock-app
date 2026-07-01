import streamlit as st
import json
import os
import pandas as pd

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")
st.title("📊 AI 智能投資決策儀表板")

# 紅綠色彩格式化函式
def color_negative_red(val):
    try:
        num = float(val)
        return f'color: {"red" if num > 0 else "green"}'
    except:
        return ''

# 讀取數據函式 (修正版：具備除錯資訊)
def load_data():
    # 針對 Streamlit Cloud 的專屬路徑修正
    possible_paths = [
        "market_data.json",                               
        "/mount/src/my-stock-app/market_data.json",       
        os.path.join(os.path.dirname(__file__), "market_data.json")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f), path
    return None, None

# 執行載入
data, used_path = load_data()

# 搜尋列
stock_code = st.sidebar.text_input("輸入台股代碼")
if st.sidebar.button("開始分析"):
    if data is None:
        st.error("❌ 找不到 market_data.json，請檢查 GitHub 自動化流程是否已推送。")
        st.write("系統檢查目錄內容:", os.listdir('.') if os.path.exists('.') else "無法存取目錄")
    else:
        st.success(f"✅ 資料載入成功 (來源: {used_path})")
        
        # 1. & 2. 關鍵數據區塊
        st.subheader("核心數據")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("即時股價", data.get("price", "-"))
        col2.metric("每股淨值", data.get("bvps", "-"))
        col3.metric("預估營收", data.get("est_revenue", "-"))
        col4.metric("預估 EPS", data.get("est_eps", "-"))
        col5.metric("預估股利", data.get("est_dividend", "-"))
        col6.metric("10日資券比", f"{data.get('margin_ratio', 0)}%")

        # 4. 今/去年每季報表
        st.subheader("今年與去年每季財報")
        if "financials" in data:
            st.dataframe(pd.DataFrame(data["financials"]).T, use_container_width=True)

        # 5. 法人買賣超
        st.subheader("三大法人買賣超 (10日)")
        if "institutional_investors" in data:
            df_inst = pd.DataFrame(data["institutional_investors"])
            st.dataframe(df_inst.style.map(color_negative_red, subset=['買賣超']), use_container_width=True)

        # 6. 主力券商買賣
        st.subheader("10日主力券商買賣")
        if "top_brokers" in data:
            st.dataframe(pd.DataFrame(data["top_brokers"]), use_container_width=True)

        # 8. 即時新聞
        st.subheader("即時新聞")
        for news in data.get("news", []):
            st.write(f"• {news}")

        # 7. AI 財報預測
        st.subheader("AI 財報預測")
        st.info(data.get("ai_prediction", "分析中..."))
else:
    st.info("請輸入代碼並搜尋。")
