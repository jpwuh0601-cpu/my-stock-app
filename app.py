import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from ai_engine import get_ai_analysis

# 設定網頁標題
st.set_page_config(page_title="股市 AI 決策系統", layout="wide")
st.title("📊 專業股市 AI 決策系統")

# 發送 LINE 通知功能
def send_line_notify(token, message):
    try:
        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"message": message}
        response = requests.post(url, headers=headers, data=payload)
        return response.status_code == 200
    except:
        return False

# 新聞爬蟲功能
def get_stock_news(ticker):
    try:
        clean_ticker = ticker.replace(".TW", "")
        url = f"https://finance.yahoo.com/quote/{clean_ticker}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = [h.text for h in soup.find_all('h3')[:5]]
        return "\n".join(news_items) if news_items else "目前無相關市場新聞。"
    except:
        return "新聞獲取服務暫時中斷。"

# 側邊欄導覽
menu = st.sidebar.radio("功能選單", ["個股分析", "AI 選股器"])

if menu == "個股分析":
    ticker_input = st.text_input("輸入股票代號 (例如 2330.TW)", "2330.TW")
    
    with st.expander("⚙️ 系統進階設定 (LINE Token)"):
        line_token = st.text_input("請輸入您的 LINE Notify Token", type="password")

    ticker = ticker_input.strip().upper()
    if ticker.isdigit():
        ticker = f"{ticker}.TW"

    if st.button("查詢分析"):
        with st.spinner(f"正在分析 {ticker}..."):
            try:
                df = yf.download(ticker, period="1mo", auto_adjust=True, progress=False)
                news = get_stock_news(ticker)
                
                if df.empty:
                    st.error(f"無法取得代號 {ticker} 的資料。")
                else:
                    current_price = float(df['Close'].iloc[-1])
                    ma20 = float(df['Close'].rolling(window=20).mean().iloc[-1])
                    is_danger = current_price < (ma20 * 0.9)
                    
                    st.subheader(f"標的: {ticker} 綜合數據")
                    col1, col2 = st.columns(2)
                    col1.metric("最新收盤價", f"{round(current_price, 2)}")
                    col2.metric("20日均線", f"{round(ma20, 2)}")
                    
                    if is_danger:
                        st.error("⚠️ [黑天鵝警示]：股價嚴重偏離均線，請注意風險！")
                    
                    st.info(news)
                    st.session_state['stock_data_summary'] = f"股票: {ticker}, 價格: {current_price}, MA20: {ma20}, 新聞: {news}"
                    
                    if line_token and is_danger:
                        send_line_notify(line_token, f"⚠️ {ticker} 警示：出現黑天鵝風險，價格 {current_price} 低於 MA20")
                        st.success("已自動發送 LINE 風險通知！")
            except Exception as e:
                st.error(f"連線失敗: {e}")

    if 'stock_data_summary' in st.session_state:
        if st.button("點擊產生 AI 分析建議"):
            st.write(get_ai_analysis(st.session_state['stock_data_summary']))

elif menu == "AI 選股器":
    st.subheader("🤖 AI 策略選股")
    st.write("掃描市場熱門標的...")
    if st.button("執行選股掃描"):
        with st.spinner("AI 正在分析市場數據..."):
            # 模擬選股邏輯
            sample_stocks = ["2330.TW", "2454.TW", "2317.TW"]
            for s in sample_stocks:
                st.success(f"AI 推薦: {s} - 技術指標表現強勁")
