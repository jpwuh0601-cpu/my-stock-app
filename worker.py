import yfinance as yf
import time
import random
import streamlit as st
import pandas as pd

@st.cache_data(ttl=3600)
def fetch_institutional_data(ticker_symbol):
    """
    模擬獲取三大法人十日買賣超細項 (實際環境建議串接 twstock 套件)
    """
    # 模擬資料生成
    data = {
        "日期": pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%m-%d'),
        "外資買賣超": [random.randint(-5000, 5000) for _ in range(10)],
        "投信買賣超": [random.randint(-1000, 1000) for _ in range(10)],
        "自營商買賣超": [random.randint(-800, 800) for _ in range(10)]
    }
    return pd.DataFrame(data).sort_values(by="日期", ascending=False)

@st.cache_data(ttl=3600)
def fetch_top_brokers_data(ticker_symbol):
    """
    模擬獲取主力十家券商十日買賣超細項
    """
    brokers = [f"券商分點_{i}" for i in range(1, 11)]
    data = {broker: [random.randint(-200, 500) for _ in range(10)] for broker in brokers}
    data["日期"] = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%m-%d')
    return pd.DataFrame(data).sort_values(by="日期", ascending=False)
