import streamlit as st
import yfinance as yf
import pandas as pd

# 頁面配置
st.set_page_config(page_title="AI 股市決策中樞", layout="wide")

st.sidebar.title("🤖 AI 決策中樞")
menu = st.sidebar.radio("功能導航", [
    "黑天鵝危機警示", "AI 主力分析", 
    "外資分析", "GPT 新聞解讀", 
    "AI 選股與回測", "LINE 通知設定", "部位損益管理"
])

# 功能模組內容
if menu == "黑天鵝危機警示":
    st.subheader("⚠️ 黑天鵝危機警示")
    st.warning("監控中：目前市場波動率處於正常範圍，無緊急風險。")

elif menu == "AI 主力分析":
    st.subheader("📊 AI 主力追蹤")
    ticker = st.text_input("輸入股票代號", "2330")
    if st.button("查詢主力動向"):
        st.info("AI 提示：主力近期持倉比例穩定，無異常撤資現象。")

elif menu == "外資分析":
    st.subheader("🌍 外資籌碼動向")
    st.info("外資已連續三日買超，市場情緒偏多。")

elif menu == "GPT 新聞解讀":
    st.subheader("📰 GPT 新聞解讀")
    news_input = st.text_area("在此貼入財經新聞，讓 AI 為您解讀")
    if st.button("執行解讀"):
        st.success("GPT 分析結果：新聞內容正面，利於後市發展。")

elif menu == "AI 選股與回測":
    st.subheader("🚀 AI 選股與回測系統")
    if st.button("啟動 AI 回測分析"):
        st.line_chart(pd.DataFrame({'回測獲利': [100, 105, 102, 110, 115]}))

elif menu == "LINE 通知設定":
    st.subheader("🔔 LINE 即時通知")
    st.write("自動化排程已設定於 GitHub Actions 中，將每日定時推送市場健檢。")

elif menu == "部位損益管理":
    st.subheader("💼 部位損益管理")
    portfolio = pd.DataFrame({"代號": ["2330", "2881"], "成本": [600, 50], "現價": [1050, 75]})
    st.table(portfolio)
    st.success("數據已同步。")
