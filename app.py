import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="專業股市決策儀表板", layout="centered")

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def main():
    st.title("📈 專業股市決策儀表板")
    data = load_data()
    ticker = st.text_input("輸入股票代號", "2330.TW")
    
    if ticker in data:
        s = data[ticker]
        
        # 1 & 2. 股價與基本面
        st.metric("即時股價", s.get('price', 0))
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨值", s.get('nav', 0))
        c2.metric("本益比", s.get('pe', 0))
        c3.metric("EPS", s.get('eps', 0))

        # 10 & 3. 技術指標圖表化
        st.subheader("📉 技術指標趨勢")
        tech_df = pd.DataFrame({
            "指標": ["KD", "MACD", "RSI"],
            "數值": [s.get('kd', 50), s.get('macd', 0), s.get('rsi', 50)]
        })
        fig = px.bar(tech_df, x="指標", y="數值", color="指標", title="技術指標現況")
        st.plotly_chart(fig)

        # 4. 法人籌碼趨勢圖
        st.subheader("🏛️ 三大法人籌碼趨勢")
        inst_data = s.get('institutional_data', [])
        if inst_data:
            df_inst = pd.DataFrame(inst_data)
            fig_inst = px.line(df_inst, x="日期", y=["外資", "投信", "自營商"], title="近十日法人買賣超走勢")
            st.plotly_chart(fig_inst)

        # 5~9. 其餘欄位 (保持原邏輯)
        st.subheader("🔮 AI 財報預測")
        st.success(s.get('ai_prediction', '數據分析中...'))
        
        st.subheader("🦢 黑天鵝警示")
        st.info(s.get('black_swan', '安全'))

    else:
        st.warning("請先執行 main_task.py 更新數據，或檢查代號是否正確。")

if __name__ == "__main__":
    main()
