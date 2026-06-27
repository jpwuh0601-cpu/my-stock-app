import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from ai_engine import get_ai_analysis

# 設定網頁標題
st.set_page_config(page_title="股市 AI 決策系統", layout="wide")
st.title("📊 專業股市 AI 決策系統")

# 新聞爬蟲功能：抓取 Yahoo 財經新聞標題
def get_stock_news(ticker):
    try:
        # 移除 .TW 以符合 Yahoo 國際版新聞路徑
        clean_ticker = ticker.replace(".TW", "")
        url = f"https://finance.yahoo.com/quote/{clean_ticker}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 抓取新聞標題
        news_items = [h.text for h in soup.find_all('h3')[:5]]
        return "\n".join(news_items) if news_items else "目前無相關市場新聞。"
    except:
        return "新聞獲取服務暫時中斷。"

# 輸入區塊
ticker_input = st.text_input("輸入股票代號 (例如 2330.TW)", "2330.TW")

# 整理代號格式
ticker = ticker_input.strip().upper()
if ticker.isdigit():
    ticker = f"{ticker}.TW"

if st.button("查詢分析"):
    with st.spinner(f"正在為您整合 {ticker} 的股價與新聞數據..."):
        try:
            # 獲取股價數據
            df = yf.download(ticker, period="1mo", auto_adjust=True, progress=False)
            news = get_stock_news(ticker)
            
            if df.empty:
                st.error(f"無法取得代號 {ticker} 的資料。")
            else:
                # 取得最新收盤價與計算 MA20
                current_price = float(df['Close'].iloc[-1])
                ma20 = float(df['Close'].rolling(window=20).mean().iloc[-1])
                trend = "多頭" if current_price > ma20 else "空頭"
                
                # 顯示結果
                st.subheader(f"標的: {ticker} 綜合數據")
                col1, col2 = st.columns(2)
                col1.metric("最新收盤價", f"{round(current_price, 2)}")
                col2.metric("20日均線", f"{round(ma20, 2)}")
                st.write(f"### 趨勢狀態: {trend}")
                
                # 顯示新聞
                st.subheader("📰 市場最新動態")
                st.info(news)
                
                # 更新狀態給 AI 使用
                st.session_state['stock_data_summary'] = f"股票: {ticker}, 最新收盤價: {current_price}, 20日均線: {ma20}, 趨勢: {trend}, 相關新聞: {news}"
                st.success("資料與新聞抓取成功！")
                
        except Exception as e:
            st.error(f"連線失敗，請稍後再試。系統錯誤代碼: {e}")

# AI 分析區塊
st.markdown("---")
st.markdown("### 🤖 AI 深度解讀")

if 'stock_data_summary' in st.session_state:
    if st.button("點擊產生 AI 分析建議"):
        with st.spinner("AI 正在綜合股價數據與市場新聞進行深度解讀..."):
            try:
                analysis_result = get_ai_analysis(st.session_state['stock_data_summary'])
                st.write(analysis_result)
            except Exception as e:
                st.error("AI 分析服務暫時無法回應，請稍後再試。")
else:
    st.info("請先輸入股票代號並查詢，以進行 AI 分析。")
