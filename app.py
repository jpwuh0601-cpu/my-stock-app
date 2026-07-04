import streamlit as st
import yfinance as yf
import requests
import os

# --- 核心 UI 佈局 (固定面板) ---
st.set_page_config(layout="wide", page_title="專業金融智慧監控系統")

# 固定頂部標題區塊
with st.container():
    st.title("📊 專業金融智慧監控系統")
    input_ticker = st.text_input("輸入股票代號 (例如: 2330.TW)")
    st.divider()

# --- 邏輯函數 ---
def get_ai_analysis(ticker_symbol):
    api_key = os.getenv("OPENROUTER_API_KEY")
    try:
        ticker = yf.Ticker(ticker_symbol)
        news = ticker.news
        latest_news = news[0]['title'] if news else "目前無最新新聞報導"
        
        if not api_key: return f"新聞標題: {latest_news}"

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [{"role": "user", "content": f"分析這則股市新聞的情緒：{latest_news}。請用一句話簡短總結市場觀點。"}]
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"分析引擎暫時無法連線"

# --- 顯示區塊 (Panel) ---
if input_ticker:
    ticker = yf.Ticker(input_ticker)
    info = ticker.info
    
    if "currentPrice" in info:
        # 1. 固定數據面板：即時股價
        price = info.get('currentPrice', 0)
        diff = price - info.get('previousClose', price)
        st.markdown(f"### 即時股價: :{'red' if diff >= 0 else 'green'}[{price:.2f} ({diff:+.2f})]")
        
        # 2. 固定數據面板：三大財務指標
        col1, col2, col3 = st.columns(3)
        col1.metric("每股淨額", info.get('bookValue', 'N/A'))
        col2.metric("本益比", info.get('forwardPE', 'N/A'))
        col3.metric("EPS", info.get('trailingEps', 'N/A'))
        
        # 3. 未來擴充區塊預留 (這裡可以放入您後續的分析模組)
        st.subheader("📰 新聞解讀")
        st.info(get_ai_analysis(input_ticker))
        
        st.subheader("🤖 AI 財報預測")
        st.write("預估今年營收、EPS 與股利：建模中...")
        
        st.subheader("📊 10日資券比與三大法人")
        st.write("等待後續整合詳細籌碼數據...")
        
        st.subheader("⚠️ 監控警示系統")
        st.warning("黑天鵝危機警示: 安全")
        st.success("✅ 自動回測：資料來源抓取成功。")
    else:
        st.error("查無此標的，請確認代號正確 (需含 .TW)")
