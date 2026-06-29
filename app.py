import streamlit as st
import json
import pandas as pd
import os

st.set_page_config(page_title="AI 投資決策儀表板", layout="wide")

st.title("📊 AI 投資決策儀表板")

# 假設資料結構已包含上述所有數據
def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return None

data = load_data()

if data:
    # 1. 即時股價與 2. 每股淨值
    col1, col2 = st.columns(2)
    col1.metric("即時股價", f"${data['price']}", delta=f"{data['change']}%")
    col2.metric("每股淨值 (BVPS)", f"${data['bvps']}")

    # 4. 今年與去年每季財報
    st.subheader("📋 季度財務報表")
    st.table(pd.DataFrame(data['financials']))

    # 5. 三大法人買賣超 (10日)
    st.subheader("🏢 三大法人買賣超 (近10日)")
    # 使用紅色表示賣超(負數)，綠色表示買超(正數) - 依台股習慣定義
    def color_negative_red(val):
        color = 'red' if val < 0 else 'green'
        return f'color: {color}'
    
    st.dataframe(pd.DataFrame(data['institutional_investors']).style.applymap(color_negative_red))

    # 6. 主力券商買賣與 10日資券比
    st.subheader("📈 主力券商與籌碼監控")
    st.metric("10日資券比", f"{data['margin_ratio']}%")
    st.table(pd.DataFrame(data['top_brokers']))

    # 3. 即時新聞與 7. AI 財報預測
    st.subheader("📰 市場動態與 AI 預測")
    st.info(f"**AI 財報預測與建議**: {data['ai_prediction']}")
    st.write("**即時新聞**:")
    for news in data['news']:
        st.write(f"- {news}")

else:
    st.warning("請執行自動化任務以載入數據。")
