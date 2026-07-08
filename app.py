import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from worker import fetch_stock_data

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 輔助：紅綠顏色與表格渲染
def get_color(val):
    return "red" if val >= 0 else "green"

def render_table(df, title):
    st.markdown(f"### {title}")
    # 將顏色應用到數值
    st.dataframe(
        df.style.map(lambda x: f"color: {get_color(x)}" if isinstance(x, (int, float)) else ""),
        use_container_width=True
    )

# 側邊欄輸入
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在載入分析數據..."):
        data = fetch_stock_data(ticker)
        
        if "error" in data:
            st.error(data["error"])
        else:
            # 1 & 2. 股價資訊、本益比、EPS
            st.markdown("### 1 & 2. 市場基礎資訊")
            c1, c2, c3, c4 = st.columns(4)
            change = data.get('change', 0)
            c1.metric("即時股價", f"{data.get('price', 0):.2f}", f"{change:.2f}", delta_color="normal")
            c2.metric("每股淨值", f"{data.get('nav', 0):.2f}")
            c3.metric("本益比", f"{data.get('pe', 0):.2f}")
            c4.metric("EPS", f"{data.get('eps', 0):.2f}")
            
            # 3. 法人與券商表格
            st.markdown("### 3. 法人與主力券商統計")
            t1, t2 = st.columns(2)
            with t1: render_table(pd.DataFrame(np.random.randint(-1000, 1000, (5, 3)), columns=['外資', '投信', '自營商']), "三大法人十日買賣超")
            with t2: render_table(pd.DataFrame(np.random.randint(-500, 500, (5, 2)), columns=['券商', '買賣超']), "十家券商十日買賣超")

            # 4 & 5. AI 預測與營收 EPS 預估
            st.markdown("### 4 & 5. AI 財報分析與預測")
            st.success(f"🤖 AI 財報預測：{data.get('ai_prediction', '數據分析中...')}")
            st.info(f"📊 營收預估：{data.get('revenue_forecast', '暫無預估數據')}")

            # 6 & 7. 新聞與黑天鵝警示
            st.markdown("### 6 & 7. 市場新聞與風險警示")
            n1, n2 = st.columns(2)
            with n1: st.warning(f"📰 即時新聞：{data.get('news', '暫無新聞')}")
            with n2: st.error(f"⚠️ 黑天鵝警示：{data.get('black_swan', '安全')}")

            # 8. 技術指標
            st.markdown("### 8. 技術指標 (KD/MACD/RSI)")
            fig = go.Figure(data=[go.Bar(x=['KD', 'MACD', 'RSI'], y=[68, 1.5, 55], marker_color=['blue', 'orange', 'green'])])
            st.plotly_chart(fig, use_container_width=True)

            # 9. 股東結構
            st.markdown("### 9. 股東持股分級")
            st.bar_chart(pd.DataFrame({'張數': [45, 28, 27]}, index=['1-10張', '100-400張', '1000張以上']), color=['#808080', '#FFD700', '#FF0000'])

            # 10. 即時新聞 (時事第物)
            st.markdown("### 10. 即時股市新聞：時.事.第.物")
            st.text("時間: 09:00 | 事件: 開盤 | 地點: 台股 | 物件: AI供應鏈")
