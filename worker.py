import streamlit as st
import yfinance as yf
import time

st.set_page_config(layout="wide", page_title="即時金融查詢器")
st.title("📊 即時金融查詢器")

# 側邊輸入框
with st.sidebar:
    st.header("手動查詢設定")
    ticker_input = st.text_input("輸入股票代號 (例如: 2330.TW)", placeholder="2330.TW")
    query_btn = st.button("立即查詢")

# 查詢邏輯
if query_btn and ticker_input:
    with st.spinner(f"正在連線 Yahoo Finance 取得 {ticker_input}..."):
        try:
            # 增加強制冷卻，避免被伺服器判定為惡意攻擊 (Rate Limiting)
            time.sleep(1.5)
            
            ticker = yf.Ticker(ticker_input)
            info = ticker.info
            
            # 檢查是否抓到資料
            if 'currentPrice' not in info and 'regularMarketPrice' not in info:
                st.error("查無此代號，請確認是否為正確的 Yahoo Finance 格式。")
            else:
                price = info.get('currentPrice') or info.get('regularMarketPrice')
                
                # 顯示資訊
                col1, col2, col3 = st.columns(3)
                col1.metric("即時股價", f"{price:.2f}")
                col2.metric("本益比", f"{info.get('forwardPE', 0):.2f}")
                col3.metric("EPS", f"{info.get('trailingEps', 0):.2f}")
                
                st.success(f"成功取得 {ticker_input} 最新資訊！")
                
                # AI 分析提示
                with st.expander("AI 快速觀點"):
                    st.write("如需 AI 詳細分析，請確保 OpenRouter API Key 已設定。")
                    
        except Exception as e:
            st.error(f"連線異常: {e}")
            st.warning("若持續出現錯誤，代表該雲端 IP 目前被限制，請稍候 30-60 秒再試。")

st.markdown("---")
st.caption("提示：本頁面為「即時手動查詢」模式。若您需要長期穩定監控，建議還是將標的放入 tickers.txt 透過後端抓取。")
