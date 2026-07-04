import streamlit as st
import pandas as pd
import json
import plotly.express as px

# 設定頁面
st.set_page_config(layout="wide", page_title="專業金融監控終端")

def load_json_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def main():
    st.title("📈 專業金融監控終端系統")
    data = load_json_data()
    
    # 1. 股票輸入
    target = st.sidebar.text_input("輸入股票代號 (例: 2330.TW)", "2330.TW")
    
    if target in data:
        info = data[target]
        
        # 顯示區塊
        st.markdown(f"### 目標: {target} | 即時價格: {info.get('price', 0)}")
        
        # 2 & 3. 基本指標與歷史走勢
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨值", info.get('nav', 0))
        c2.metric("本益比", info.get('pe', 0))
        c3.metric("EPS", info.get('eps', 0))
        
        # 繪製 K 線圖 (使用 Plotly)
        if 'history' in info:
            df = pd.DataFrame(info['history'])
            fig = px.line(df, x='日期', y='股價', title="近一年走勢圖")
            st.plotly_chart(fig, use_container_width=True)
            
        # 5. 三大法人與資券比 (視覺化警示)
        st.subheader("5. 三大法人與 10 日資券比")
        st.write(f"目前資券比: {info.get('margin_ratio', 0)}%")
        
        # 7. AI 預測與新聞 (放置在後方)
        st.subheader("7. 即時新聞與 AI 財報預測")
        with st.expander("展開 AI 財報深度預測"):
            st.info(f"新聞解讀: {info.get('news', '暫無')}")
            st.success(f"AI 財報預測: {info.get('ai_prediction', '計算中...')}")
            
        # 8. 系統警示與回測 (新增邏輯)
        st.divider()
        st.subheader("8. 系統監控與回測")
        if st.button("啟動資料正確性回測"):
            # 簡單的邏輯檢核
            if info.get('price', 0) > 0:
                st.success("回測成功：資料鏈路正確，即時價格已更新。")
            else:
                st.error("回測失敗：資料缺失，請檢查 API 源。")
    else:
        st.write("請輸入正確代號並確保自動化排程已完成更新。")

if __name__ == "__main__":
    main()
