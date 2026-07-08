import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.subplots as sp

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 1. 股東分級圖表函式 (新增需求)
def plot_shareholder_structure():
    st.markdown("### 📊 股東人數與持股分級統計")
    # 模擬數據：各持股分級人數
    levels = ["1-10張", "10-100張", "100-400張", "400-1000張", "1000張以上"]
    counts = [5000, 2000, 800, 300, 150]
    # 指定顏色：1-10張灰色，100-400張黃色，1000張以上紅色
    colors = ["#A9A9A9", "#D3D3D3", "#FFD700", "#FFA500", "#FF0000"]
    
    fig = go.Figure(data=[go.Bar(
        x=levels, 
        y=counts,
        marker_color=colors
    )])
    fig.update_layout(title="持股比例分級結構", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# 2. 籌碼大戶分析 (維持原有的邏輯)
def plot_smart_money(data_df):
    st.markdown("### 📊 籌碼動向 (大戶 >400張)")
    fig = go.Figure()
    for col in ["外資", "投信", "自營商"]:
        big_money = np.where(data_df[col] > 400, data_df[col], 0)
        small_money = np.where(data_df[col] <= 400, data_df[col], 0)
        fig.add_trace(go.Bar(x=data_df["日期"], y=big_money, name=f"{col} (大戶)", marker_color='red'))
        fig.add_trace(go.Bar(x=data_df["日期"], y=small_money, name=f"{col} (散戶)", marker_color='green'))
    fig.update_layout(barmode='stack', height=300)
    st.plotly_chart(fig, use_container_width=True)

# 主程式邏輯
ticker = st.text_input("輸入股票代號 (例如: 2330)", "2330")
if st.button("查詢分析數據"):
    dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%m-%d')
    
    # 呼叫新增的股東分級圖表
    plot_shareholder_structure()
    
    # 原有的籌碼圖表
    inst_data = pd.DataFrame({"日期": dates, "外資": np.random.randint(-1500, 1500, 10), "投信": np.random.randint(-600, 600, 10), "自營商": np.random.randint(-400, 400, 10)})
    plot_smart_money(inst_data)
    
    st.success("籌碼分析完成，大戶籌碼已透過柱狀體顏色標記完畢。")
