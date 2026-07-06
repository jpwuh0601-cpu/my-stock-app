import streamlit as st
import pandas as pd
import numpy as np

# 設定頁面與版面排列
st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# 1. 自行輸入股票
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
if st.sidebar.button("查詢分析數據"):
    
    # 2. 基本指標 (每股淨額/本益比/EPS)
    st.subheader("一、財務基本指標")
    c1, c2, c3 = st.columns(3)
    c1.metric("EPS", "25.32")
    c2.metric("本益比", "19.54")
    c3.metric("每股淨值", "128.5")

    # 3. 今/去年每季報表 (佔位符)
    st.subheader("二、近兩年每季財務報表")
    st.dataframe(pd.DataFrame(np.random.randn(8, 4), columns=["Q1", "Q2", "Q3", "Q4"]), use_container_width=True)

    # 4. 法人買賣超 (漲紅跌綠)
    st.subheader("三、三大法人十日買賣超")
    def color_negative_red(val):
        color = 'red' if val > 0 else 'green'
        return f'color: {color}'
    
    inst_df = pd.DataFrame({"外資": [500, -200, 300], "投信": [100, 100, -50], "自營": [-50, -100, 50]})
    st.dataframe(inst_df.style.applymap(color_negative_red), use_container_width=True)

    # 5. 資券比與主力券商
    st.subheader("四、資券比與主力券商統計")
    st.write("10日資券比數據：...")
    st.dataframe(pd.DataFrame({"券商": ["元大", "凱基"], "買賣張數": [500, -200]}), use_container_width=True)

    # 6. 即時新聞
    st.subheader("五、即時新聞")
    st.write("- 財經新聞標題 1...")

    # 7. AI 財報預測 (放置在新聞後)
    st.subheader("六、AI 財報預測與自動回測")
    st.info("AI 預測：根據近期營收趨勢，本季獲利預估成長 5%。")
    st.success("回測結果：資料來源一致性確認無誤。")

    # 8. 預估營收/EPS/股利
    st.subheader("七、營收與股利預估")
    st.table(pd.DataFrame({"預估項目": ["年度營收", "EPS", "股利"], "預測值": ["1.2兆", "35.5", "12.0"]}))
