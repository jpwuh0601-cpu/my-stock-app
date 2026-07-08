import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="專業股市決策儀表板", layout="centered")

def load_data():
    try:
        if not os.path.exists("market_data.json"):
            return {}
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def main():
    st.title("📈 專業股市決策儀表板")
    data = load_data()

    if not data:
        st.error("無法讀取市場數據，請檢查 market_data.json 是否正常更新。")
        return

    ticker_input = st.text_input("輸入股票代號", "2330.TW")
    if st.button("查詢股價"):
        st.session_state.current_ticker = ticker_input

    ticker = st.session_state.get("current_ticker", ticker_input)
    
    if ticker in data:
        s = data[ticker]
        
        # 使用 .get 預設值防止 KeyError
        st.subheader(f"股票代號: {ticker}")
        st.metric("即時股價", s.get('price', 'N/A'))

        # 基本面 (確保有值才顯示)
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨值", s.get('nav', 0))
        c2.metric("本益比", s.get('pe', 0))
        c3.metric("EPS", s.get('eps', 0))

        # 籌碼面 (加入 DataFrame 格式檢查)
        st.subheader("🏛️ 三大法人十日買賣超")
        inst_data = s.get('institutional_data', [])
        if isinstance(inst_data, list) and len(inst_data) > 0:
            st.dataframe(pd.DataFrame(inst_data))
        else:
            st.write("尚無籌碼數據")

        # 其他欄位同理，改用 s.get('key', '預設值')
        st.success(f"AI 分析報告: {s.get('ai_report', '分析中...')}")

    else:
        st.warning("查無此代號數據。")

if __name__ == "__main__":
    main()
