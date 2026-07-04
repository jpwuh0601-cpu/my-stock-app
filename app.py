import streamlit as st
import yfinance as yf
import requests
import os

# --- 設定頁面 ---
st.set_page_config(layout="wide", page_title="即時金融查詢終端")
st.title("🔍 專業金融即時查詢終端")

# --- AI 分析邏輯 (內嵌) ---
def get_ai_analysis(ticker_symbol):
    api_key = os.getenv("OPENROUTER_API_KEY")
    try:
        ticker = yf.Ticker(ticker_symbol)
        # 確保抓取到新聞
        news = ticker.news
        latest_news = news[0]['title'] if news and len(news) > 0 else "目前無最新新聞報導"
        
        if not api_key:
            return f"【最新新聞標題】: {latest_news} (提示: 請在 Streamlit Secrets 設定 OPENROUTER_API_KEY)"

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [{"role": "user", "content": f"分析這則股市新聞的情緒：{latest_news}。請用一句話簡短總結市場觀點。"}]
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"AI 分析引擎發生錯誤: {str(e)}"

# --- 輸入查詢區 ---
input_ticker = st.text_input("請輸入股票代號 (例如: 2330.TW)", placeholder="輸入後按下 Enter")

if input_ticker:
    with st.spinner(f"正在即時查詢 {input_ticker}..."):
        try:
            ticker = yf.Ticker(input_ticker)
            info = ticker.info
            
            # 若 currentPrice 為 None，代表抓不到資料
            if info.get("currentPrice") is None:
                st.error(f"無法獲取 {input_ticker} 的即時數據，請檢查代號是否正確。")
            else:
                # 顯示數據
                st.success(f"成功獲取 {input_ticker} 資訊")
                col1, col2, col3 = st.columns(3)
                col1.metric("即時價格", f"{info.get('currentPrice', 0):.2f}")
                col2.metric("EPS", info.get("trailingEps", "N/A"))
                col3.metric("本益比", info.get("forwardPE", "N/A"))
                
                # 顯示 AI 分析
                st.subheader("🤖 AI 市場解讀")
                with st.spinner("AI 正在深度思考中..."):
                    st.info(get_ai_analysis(input_ticker))
                
                # 顯示圖表
                st.subheader("📈 歷史走勢")
                hist = ticker.history(period="1mo")
                if not hist.empty:
                    st.line_chart(hist['Close'])
                else:
                    st.warning("查無歷史成交資訊。")
        except Exception as e:
            st.error(f"系統錯誤: {str(e)}")
