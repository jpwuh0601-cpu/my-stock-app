import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from openai import OpenAI
import plotly.graph_objects as go

# ... (前面的程式碼與之前一樣) ...

def get_ai_summary(ticker_name, data):
    # 將技術指標數據加入 AI 的 prompt
    sma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
    last_price = data['Close'].iloc[-1]
    
    context = f"股票: {ticker_name}, 最新價格: {last_price:.2f}, 20日均線: {sma_20:.2f}"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"請分析以下數據趨勢: {context}. 並根據價格與均線關係給出簡短建議。"}]
    )
    return response.choices[0].message.content

# ... (主邏輯中呼叫 get_ai_summary(ticker, df)) ...
