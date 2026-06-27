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

# 輸入區塊
ticker_input = st.text_input("輸入股票代號 (例如 2330.TW)", "2330.TW")

# 設定區塊 (隱藏式設定)
with st.expander("⚙️ 系統進階設定 (LINE Token)"):
    line_token = st.text_input("請輸入您的 LINE Notify Token", type="password")

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
                # 計算數據
                current_price = float(df['Close'].iloc[-1])
                ma20 = float(df['Close'].rolling(window=20).mean().iloc[-1])
                trend = "多頭" if current_price > ma20 else "空頭"
                
                # 黑天鵝警示邏輯 (跌破 MA20 的 10% 即警示)
                is_danger = current_price < (ma20 * 0.9)
                
                # 顯示結果
                st.subheader(f"標的: {ticker} 綜合數據")
                col1, col2 = st.columns(2)
                col1.metric("最新收盤價", f"{round(current_price, 2)}")
                col2.metric("20日均線", f"{round(ma20, 2)}")
                
                if is_danger:
                    st.error("⚠️ [黑天鵝警示]：股價嚴重偏離均線，請注意風險！")
                
                st.write(f"### 趨勢狀態: {trend}")
                
                # 顯示新聞
                st.subheader("📰 市場最新動態")
                st.info(news)
                
                # 更新狀態給 AI 使用
                st.session_state['stock_data_summary'] = f"股票: {ticker}, 最新收盤價: {current_price}, 20日均線: {ma20}, 趨勢: {trend}, 相關新聞: {news}"
                st.success("資料抓取成功！")
                
                # 自動觸發 LINE 通知
                if line_token and is_danger:
                    if send_line_notify(line_token, f"⚠️ {ticker} 警示：出現黑天鵝風險，價格 {current_price} 低於 MA20"):
                        st.success("已自動發送 LINE 風險通知！")
                    else:
                        st.error("LINE 通知發送失敗，請檢查 Token 是否正確。")
                
        except Exception as e:
            st.error(f"連線失敗，系統錯誤代碼: {e}")

# AI 分析區塊
st.markdown("---")
st.markdown("### 🤖 AI 深度解讀")

if 'stock_data_summary' in st.session_state:
    if st.button("點擊產生 AI 分析建議"):
        with st.spinner("AI 正在綜合股價與新聞進行深度解讀..."):
            try:
                analysis_result = get_ai_analysis(st.session_state['stock_data_summary'])
                st.write(analysis_result)
            except Exception as e:
                st.error("AI 分析服務暫時無法回應，請稍後再試。")
else:
    st.info("請先輸入股票代號並查詢，以進行 AI 分析。")
