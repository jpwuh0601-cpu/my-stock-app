import streamlit as st
import pandas as pd
import plotly.express as px
import os
import yfinance as yf
from datetime import datetime
from openai import OpenAI

# 設定頁面風格
st.set_page_config(page_title="AI 專業投資儀表板", layout="wide", page_icon="📈")

st.title("📈 AI 專業投資決策中樞 (專業版)")

# 安全讀取環境變數
client = OpenAI(
    base_url="https://openrouter.ai/api/v1", 
    api_key=st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
)

# 頁面內容
menu = st.sidebar.radio("導航目錄", ["🤖 個股深度分析", "💼 部位管理"])

if menu == "🤖 個股深度分析":
    st.subheader("個股即時數據健檢")
    t = st.text_input("輸入股票代號 (例如 2330)", "2330")
    
    if st.button("啟動專業分析"):
        with st.spinner("正在抓取完整財務數據與即時行情..."):
            try:
                # 取得股票資訊
                ticker_symbol = f"{t}.TW"
                stock = yf.Ticker(ticker_symbol)
                hist = stock.history(period="1mo")
                info = stock.info
                
                # 數據提取：即時報價與財務指標
                curr = info.get('currentPrice', 0)
                prev = info.get('previousClose', 1)
                change = ((curr - prev) / prev) * 100
                
                # 顯示即時指標面板
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("即時股價", f"{curr:.2f}", f"{change:.2f}%")
                col2.metric("本益比 (PE)", info.get('trailingPE', 'N/A'))
                col3.metric("每股淨值 (PB)", info.get('priceToBook', 'N/A'))
                col4.metric("EPS", info.get('trailingEps', 'N/A'))
                
                # 額外資訊欄
                col5, col6 = st.columns(2)
                col5.metric("發行股數", f"{info.get('sharesOutstanding', 0):,}")
                col6.metric("成交量", f"{info.get('volume', 0):,}")
                
                # AI 分析
                funda_data = {
                    "名稱": info.get('longName'),
                    "PE": info.get('trailingPE'),
                    "PB": info.get('priceToBook'),
                    "EPS": info.get('trailingEps'),
                    "產業": info.get('sector'),
                    "Beta": info.get('beta'),
                    "ProfitMargins": info.get('profitMargins')
                }
                
                prompt = f"以專業分析師角度，針對 {ticker_symbol} 進行健檢。數據如下：{funda_data}。請從基本面評估、合理估值與投資機會進行綜合分析。"
                response = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
                
                st.markdown("---")
                st.markdown("### 🎯 AI 深度健檢報告")
                st.write(response.choices[0].message.content)
                
                # 技術指標圖表
                st.markdown("### 📊 近期股價走勢")
                st.line_chart(hist['Close'])

            except Exception as e:
                st.error(f"資料抓取失敗: {e}，請確認股票代號是否正確。")

elif menu == "💼 部位管理":
    st.subheader("我的持股看板")
    st.info("此處可擴充籌碼面分析數據整合（如：三大法人買賣超資訊）。")
