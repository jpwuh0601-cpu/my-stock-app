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
    
    # 警示邏輯：判斷 AI 分析是否包含 "賣出"
    ai_text = str(data.get("ai_prediction", ""))
    is_alert = "賣出" in ai_text
    
    # 顯示帶有警示顏色的股價
    if is_alert:
        st.markdown(f'<h1 style="color:red;">⚠️ 賣出警告: 股價 {float(data.get("price", 0)):,.2f}</h1>', unsafe_allow_html=True)
    else:
        st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    st.subheader("🏦 三大法人籌碼數據")
    
    raw = data.get("institutional_investors", [])
    
    # 視覺化邏輯：將籌碼數據繪製成長條圖
    if isinstance(raw, list) and len(raw) > 0:
        df_chart = pd.DataFrame(raw)
        if "機構" in df_chart.columns and "買賣超" in df_chart.columns:
            fig = px.bar(df_chart, x="機構", y="買賣超", title="法人籌碼分佈", color="買賣超", color_continuous_scale="RdBu")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.table(df_chart)
    else:
        st.info("目前無籌碼數據。")

    st.subheader("🤖 AI 智能分析")
    st.write(ai_text)

    with st.expander("🔍 除錯數據檢查"):
        st.json(data)

if __name__ == "__main__":
    main()
