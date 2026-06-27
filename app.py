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

# 優化資料獲取函式：增加 Timeout 與錯誤訊息反饋
def fetch_stock_data(ticker, period="1mo"):
    try:
        # 移除 threads=False 以讓系統自動調節，若卡住請保持預設
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, auto_adjust=True)
        return df
    except Exception as e:
        # 記錄錯誤而不中斷程序
        st.error(f"資料取得失敗: {ticker}")
        return pd.DataFrame()

# 發送 LINE 通知功能
def send_line_notify(token, message):
    try:
        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"message": message}
        response = requests.post(url, headers=headers, data=payload, timeout=5)
        return response.status_code == 200
    except:
        return False

# 新聞爬蟲功能
def get_stock_news(ticker):
    try:
        # 使用簡單的 yahoo finance 連結避免複雜解析
        url = f"https://finance.yahoo.com/quote/{ticker}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = [h.text for h in soup.find_all('h3')[:3]] # 縮減數量提升速度
        return "\n".join(news_items) if news_items else "目前無相關市場新聞。"
    except:
        return "新聞服務暫時離線。"

# 側邊欄導覽
menu = st.sidebar.radio("功能選單", ["個股分析", "AI 選股器", "批量比較"])

if menu == "個股分析":
    ticker_input = st.text_input("輸入股票代號 (例如 2330.TW)", "2330.TW")
    line_token = st.text_input("LINE Notify Token", type="password")

    if st.button("查詢分析"):
        with st.spinner("資料載入中..."):
            ticker = ticker_input.strip().upper()
            df = fetch_stock_data(ticker)
            
            if df.empty:
                st.error("無法取得資料，請檢查代號是否正確 (例如 2330.TW)。")
            else:
                news = get_stock_news(ticker)
                current_price = float(df['Close'].iloc[-1])
                ma20 = float(df['Close'].rolling(window=20).mean().iloc[-1])
                
                st.metric("最新收盤價", f"{round(current_price, 2)}")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='收盤價'))
                st.plotly_chart(fig, use_container_width=True)
                
                st.session_state['summary'] = f"股票: {ticker}, 價格: {current_price}, 新聞: {news}"
                st.info(news)

    if 'summary' in st.session_state and st.button("AI 深度分析"):
        st.write(get_ai_analysis(st.session_state['summary']))

elif menu == "AI 選股器":
    if st.button("執行選股掃描"):
        with st.spinner("掃描中..."):
            watch_list = ["2330.TW", "2454.TW", "2317.TW"]
            for s in watch_list:
                df = fetch_stock_data(s)
                if not df.empty and df['Close'].iloc[-1] > df['Close'].rolling(20).mean().iloc[-1]:
                    st.success(f"強勢股: {s}")

elif menu == "批量比較":
    tickers_input = st.text_input("輸入代號 (逗號分隔)", "2330.TW, 2454.TW")
    if st.button("開始比較"):
        tickers = [t.strip().upper() for t in tickers_input.split(",")]
        data = [{"代號": t, "最新價": round(float(fetch_stock_data(t)['Close'].iloc[-1]), 2)} 
                for t in tickers if not fetch_stock_data(t).empty]
        st.table(pd.DataFrame(data))
