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
                stock = yf.Ticker(f"{t}.TW")
                hist = stock.history(period="1mo")
                info = stock.info
                
                # 計算漲跌幅
                curr = info.get('currentPrice', 0)
                prev = info.get('previousClose', 1)
                change = ((curr - prev) / prev) * 100
                
                # 顯示即時儀表板
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("即時股價", f"{curr:.2f}", f"{change:.2f}%")
                col2.metric("本益比 (PE)", info.get('trailingPE', 'N/A'))
                col3.metric("每股淨值 (PB)", info.get('priceToBook', 'N/A'))
                col4.metric("EPS", info.get('trailingEps', 'N/A'))
                
                st.write(f"**發行股數**: {info.get('sharesOutstanding', 'N/A'):,}")
                
                # AI 分析
                funda_data = {
                    "PE": info.get('trailingPE'),
                    "PB": info.get('priceToBook'),
                    "EPS": info.get('trailingEps'),
                    "Beta": info.get('beta'),
                    "ProfitMargins": info.get('profitMargins')
                }
                
                prompt = f"以專業分析師角度，針對股票 {t} 進行分析，數據如下：{funda_data}。請分析基本面、本益比合理性，並提供投資策略建議。"
                response = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
                st.markdown("### 🎯 深度分析建議")
                st.write(response.choices[0].message.content)
                
                # 繪圖
                st.line_chart(hist['Close'])

            except Exception as e:
                st.error(f"資料抓取失敗: {e}")

elif menu == "💼 部位管理":
    st.subheader("我的持股看板")
    st.info("此處可擴充籌碼面分析數據整合。")
