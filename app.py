import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    # 警示邏輯
    ai_text = str(data.get("ai_prediction", ""))
    is_alert = "賣出" in ai_text
    
    if is_alert:
        st.markdown(f'<h1 style="color:red;">⚠️ 賣出警告: 股價 {float(data.get("price", 0)):,.2f}</h1>', unsafe_allow_html=True)
    else:
        st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    # 1. 時間範圍選擇器
    st.subheader("📊 股價歷史走勢")
    time_range = st.radio("選擇觀察週期", ["1個月", "3個月", "1年"], horizontal=True)
    
    # 這裡假設您的 worker.py 已抓取足夠資料，或我們進行簡單切片模擬
    # 實際運作時，建議在 worker.py 加入對應週期參數
    history = data.get("history", [])
    if history:
        df_hist = pd.DataFrame(history)
        df_hist['Date'] = pd.to_datetime(df_hist['Date'])
        
        # 簡單的過濾邏輯（基於日期切片）
        if time_range == "1個月":
            df_plot = df_hist.tail(20)
        elif time_range == "3個月":
            df_plot = df_hist.tail(60)
        else:
            df_plot = df_hist
            
        fig = px.line(df_plot, x="Date", y="Close", title=f"台積電 ({time_range}) 股價趨勢")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏦 三大法人籌碼數據")
    raw = data.get("institutional_investors", [])
    if raw:
        df_chart = pd.DataFrame(raw)
        st.bar_chart(df_chart.set_index("機構"))

    st.subheader("🤖 AI 智能分析")
    st.write(ai_text)

if __name__ == "__main__":
    main()
