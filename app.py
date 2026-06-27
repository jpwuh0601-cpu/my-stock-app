import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import plotly.graph_objects as go
from bs4 import BeautifulSoup
from ai_engine import get_ai_analysis

# 設定網頁標題
st.set_page_config(page_title="股市 AI 決策系統", layout="wide")
st.title("📊 專業股市 AI 決策系統")

# 優化後的資料獲取函式
def fetch_stock_data(ticker):
    try:
        # 增加 session 模擬與更長的 timeout 以降低請求失敗機率
        stock = yf.Ticker(ticker)
        df = stock.history(period="1mo", timeout=30)
        if df is None or df.empty:
            return None
        return df
    except Exception as e:
        return None

# 新聞爬蟲功能
def get_stock_news(ticker):
    try:
        url = f"https://finance.yahoo.com/quote/{ticker}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = [h.text for h in soup.find_all('h3')[:3]]
        return "\n".join(news_items) if news_items else "目前無相關市場新聞。"
    except:
        return "新聞服務暫時離線。"

# 側邊欄
menu = st.sidebar.radio("功能選單", ["個股分析", "AI 選股器", "批量比較"])

if menu == "個股分析":
    ticker_input = st.text_input("輸入股票代號 (例如 2330.TW)", "2330.TW")
    if st.button("查詢分析"):
        df = fetch_stock_data(ticker_input.strip().upper())
        if df is None:
            st.error(f"無法取得 {ticker_input} 資料。這通常是因為雲端環境連線受限，請稍後再試。")
        else:
            current_price = float(df['Close'].iloc[-1])
            st.metric("最新收盤價", f"{round(current_price, 2)}")
            st.info(get_stock_news(ticker_input.strip().upper()))

elif menu == "AI 選股器":
    if st.button("執行選股掃描"):
        watch_list = ["2330.TW", "2454.TW", "2317.TW"]
        results = []
        for s in watch_list:
            df = fetch_stock_data(s)
            if df is not None and df['Close'].iloc[-1] > df['Close'].rolling(20).mean().iloc[-1]:
                results.append(s)
        
        if results:
            st.success(f"強勢股: {', '.join(results)}")
        else:
            st.warning("掃描完成，但目前無符合多頭條件的標的，或數據抓取受限。")

elif menu == "批量比較":
    st.subheader("⚖️ 股票數據批量比較")
    tickers_input = st.text_input("輸入代號 (逗號分隔)", "2330.TW, 2454.TW")
    if st.button("開始比較"):
        tickers = [t.strip().upper() for t in tickers_input.split(",")]
        data = []
        for t in tickers:
            df = fetch_stock_data(t)
            if df is not None:
                data.append({"代號": t, "最新價": round(float(df['Close'].iloc[-1]), 2)})
            else:
                data.append({"代號": t, "最新價": "無法取得數據"})
        
        if data:
            st.table(pd.DataFrame(data))
