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

# 下載資料輔助函式，增加錯誤處理與容錯
def fetch_stock_data(ticker, period="1mo"):
    try:
        # 使用 threads=False 防止在 Streamlit 多執行緒環境下崩潰
        df = yf.download(ticker, period=period, auto_adjust=True, progress=False, threads=False)
        return df
    except Exception as e:
        st.error(f"下載 {ticker} 資料時發生錯誤: {e}")
        return pd.DataFrame()

# 發送 LINE 通知功能
def send_line_notify(token, message):
    try:
        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"message": message}
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        return response.status_code == 200
    except:
        return False

# 新聞爬蟲功能
def get_stock_news(ticker):
    try:
        clean_ticker = ticker.split('.')[0]
        url = f"https://finance.yahoo.com/quote/{ticker}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = [h.text for h in soup.find_all('h3')[:5]]
        return "\n".join(news_items) if news_items else "目前無相關市場新聞。"
    except:
        return "新聞獲取服務暫時中斷。"

# 側邊欄導覽
menu = st.sidebar.radio("功能選單", ["個股分析", "AI 選股器", "批量比較"])

if menu == "個股分析":
    ticker_input = st.text_input("輸入股票代號 (例如 2330.TW)", "2330.TW")
    
    with st.expander("⚙️ 系統進階設定 (LINE Token)"):
        line_token = st.text_input("請輸入您的 LINE Notify Token", type="password")

    ticker = ticker_input.strip().upper()
    
    if st.button("查詢分析"):
        with st.spinner(f"正在分析 {ticker}..."):
            df = fetch_stock_data(ticker)
            news = get_stock_news(ticker)
            
            if df.empty:
                st.error(f"無法取得代號 {ticker} 的資料，請確認代號是否正確。")
            else:
                current_price = float(df['Close'].iloc[-1])
                ma20 = float(df['Close'].rolling(window=20).mean().iloc[-1])
                is_danger = current_price < (ma20 * 0.9)
                
                st.subheader(f"標的: {ticker} 綜合數據")
                col1, col2 = st.columns(2)
                col1.metric("最新收盤價", f"{round(current_price, 2)}")
                col2.metric("20日均線", f"{round(ma20, 2)}")
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='收盤價', line=dict(color='blue')))
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'].rolling(window=20).mean(), name='20日均線', line=dict(color='orange', dash='dash')))
                st.plotly_chart(fig, use_container_width=True)
                
                if is_danger:
                    st.error("⚠️ [黑天鵝警示]：股價嚴重偏離均線，請注意風險！")
                
                st.info(news)
                st.session_state['stock_data_summary'] = f"股票: {ticker}, 價格: {current_price}, MA20: {ma20}, 新聞: {news}"
                
                if line_token and is_danger:
                    if send_line_notify(line_token, f"⚠️ {ticker} 警示：出現黑天鵝風險，價格 {current_price} 低於 MA20"):
                        st.success("已自動發送 LINE 風險通知！")
                    else:
                        st.error("LINE 通知發送失敗。")

    if 'stock_data_summary' in st.session_state:
        if st.button("點擊產生 AI 分析建議"):
            st.write(get_ai_analysis(st.session_state['stock_data_summary']))

elif menu == "AI 選股器":
    st.subheader("🤖 AI 策略選股 (多頭篩選)")
    if st.button("執行選股掃描"):
        with st.spinner("AI 正在分析市場數據..."):
            watch_list = ["2330.TW", "2454.TW", "2317.TW", "2303.TW", "2308.TW"]
            found_stocks = []
            for s in watch_list:
                df = fetch_stock_data(s)
                if not df.empty:
                    price = float(df['Close'].iloc[-1])
                    ma20 = float(df['Close'].rolling(window=20).mean().iloc[-1])
                    if price > ma20:
                        found_stocks.append(s)
            
            if found_stocks:
                for s in found_stocks:
                    st.success(f"AI 推薦 (技術面多頭): {s}")
            else:
                st.warning("目前無符合篩選條件的標的或連線逾時。")

elif menu == "批量比較":
    st.subheader("⚖️ 股票數據批量比較")
    tickers_input = st.text_input("輸入多個代號 (以逗號分隔，例如 2330.TW, 2454.TW)", "2330.TW, 2454.TW")
    if st.button("開始比較"):
        tickers = [t.strip().upper() for t in tickers_input.split(",")]
        data = []
        for t in tickers:
            df = fetch_stock_data(t)
            if not df.empty:
                data.append({
                    "代號": t,
                    "最新收盤價": round(float(df['Close'].iloc[-1]), 2),
                    "漲跌幅 (%)": round(((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100, 2)
                })
        
        if data:
            st.table(pd.DataFrame(data))
        else:
            st.error("無法取得數據，請檢查輸入代號或稍後再試。")
