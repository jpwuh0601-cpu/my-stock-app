import sys
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go

# 檢查是否讀取到套件
try:
    import yfinance
    st.sidebar.success("yfinance 已載入")
except ImportError:
    st.sidebar.error("yfinance 安裝失敗，請檢查 requirements.txt")

# ...後續程式碼
