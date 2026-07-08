import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="股市隨身看", layout="centered")

# CSS 優化：漲紅跌綠、卡片式設計
st.markdown("""
    <style>
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6; }
    .price-up { color: #ff4b4b; font-weight: bold; }
    .price-down { color: #00cc96; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

def load_data():
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def main():
    st.title("📈 專業股市決策儀表板")
    data = load_data()

    # 1. 快捷查詢
    ticker = st.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
    
    if ticker in data:
        s = data[ticker]
        
        # 顯示即時股價 (漲紅跌綠)
        change = s.get('change', 0)
        color_class = "price-up" if change >= 0 else "price-down"
        st.markdown(f"### 即時股價: <span class='{color_class}'>{s.get('price', 0)} ({change:+.2f})</span>", unsafe_allow_html=True)

        # 2. 基本面資訊
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨值", f"{s.get('nav', 0)}")
        c2.metric("本益比", f"{s.get('pe', 0)}")
        c3.metric("EPS", f"{s.get('eps', 0)}")

        # 3. 黑天鵝風險警示 (最優先呈現)
        st.subheader("🦢 地緣政治黑天鵝警示")
        st.warning("議題關注：(1) 俄烏衝突 (2) 美伊關係 (3) 聯準會利率會議")
        st.info(f"近期發展：{s.get('black_swan', '安全')}")

        # 4. 財報預測 (調整至新聞後)
        st.subheader("🔮 AI 綜合財報與營收預測")
        st.success(s.get('ai_prediction', '數據分析中...'))

        # 5. 三大法人籌碼 (漲紅跌綠)
        st.subheader("🏛️ 三大法人十日買賣超")
        df_inst = pd.DataFrame(s.get("institutional_data", []))
        st.dataframe(df_inst.style.map(lambda x: 'color: red' if x > 0 else 'color: green' if x < 0 else 'black', subset=['外資', '投信', '自營商']))

        # 6. 資券與主力 (10日)
        st.subheader("📊 10日資券與主力指標")
        st.write(f"資券比: {s.get('margin_ratio', 0)}%")
        st.write("主力券商買賣超資訊 (已更新)")

        # 7. 歷史報表切換
        st.subheader("🗓️ 季報數據")
        if st.checkbox("顯示今年與去年每季報表"):
            st.write("表格載入中...")

    else:
        st.warning("⚠️ 系統正在更新數據中，請稍候。")

if __name__ == "__main__":
    main()
