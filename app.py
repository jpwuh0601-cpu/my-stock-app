import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
import os

# 設定頁面配置
st.set_page_config(layout="wide", page_title="AI 專業金融分析終端")

def load_data(filepath):
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def main():
    st.title("📈 AI 專業金融分析終端")
    
    # 載入數據
    data = load_data("market_data.json")
    history = load_data("backtest_history.json")
    
    # 選股界面
    target = st.sidebar.text_input("輸入股票代號", "2330.TW")
    
    info = data.get(target)
    
    if not info:
        st.info("請等待自動化排程更新數據...")
        return

    # 顯示核心數據
    st.metric("即時股價", f"{info.get('price', 0)} 元")
    
    # 視覺化圖表區塊 (恢復 Plotly 渲染)
    st.subheader("📊 AI 歷史回測走勢")
    
    if target in history and "prices" in history[target]:
        prices = history[target]["prices"]
        # 使用輕量化圖表配置
        fig = go.Figure(data=go.Scatter(
            y=prices, 
            mode='lines+markers', 
            line=dict(color='#1f77b4', width=2)
        ))
        fig.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("尚無足夠回測數據繪製圖表。")

    # 籌碼與 AI 分析
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("AI 預測摘要")
        st.write(info.get('ai_prediction', '分析中...'))
    with col2:
        st.subheader("三大法人與籌碼")
        if "broker_daily" in info:
            st.dataframe(pd.DataFrame(info["broker_daily"]), hide_index=True)

if __name__ == "__main__":
    main()
