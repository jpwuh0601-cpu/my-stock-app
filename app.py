import streamlit as st
import json
import os
import sys

# 1. 最嚴謹的設定方式：確保只執行一次且放在最上方
try:
    st.set_page_config(page_title="股市儀表板", layout="wide")
except st.errors.StreamlitAPIException:
    # 若已設定過則忽略，避免錯誤崩潰
    pass

st.title("📈 專業股市決策儀表板")

# 2. 簡化資料讀取流程
json_path = "market_data.json"

if not os.path.exists(json_path):
    st.error(f"找不到數據檔案: {json_path}。請確認 GitHub Actions 已執行完畢。")
else:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        tickers = list(data.keys())
        if tickers:
            selected = st.selectbox("請選擇股票", tickers)
            
            if selected:
                d = data[selected]
                # 核心指標顯示
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("股價", d.get("price", 0))
                col2.metric("每股淨值", d.get("nav", 0))
                col3.metric("本益比", d.get("pe", 0))
                col4.metric("EPS", d.get("eps", 0))
                
                # 財務預估模型
                st.markdown("---")
                st.subheader("📊 明年財務預估模型")
                
                c1, c2 = st.columns(2)
                margin_rate = c1.slider("假設稅後淨利率 (%)", 5.0, 30.0, 15.0) / 100
                payout_rate = c2.slider("假設盈餘分配率 (%)", 30.0, 90.0, 60.0) / 100
                
                est_revenue = d.get("last_year_revenue", 1e9) * 1.12
                est_net_profit = est_revenue * margin_rate
                est_eps = est_net_profit / d.get("shares", 1e9)
                est_dividend = est_eps * payout_rate
                
                p1, p2, p3, p4 = st.columns(4)
                p1.metric("預估明年營收", f"{est_revenue/1e8:.1f} 億")
                p2.metric("預估稅後淨利", f"{est_net_profit/1e8:.1f} 億")
                p3.metric("預估 EPS", f"{est_eps:.2f}")
                p4.metric("預估現金股利", f"{est_dividend:.2f}")
        else:
            st.warning("數據庫為空。")
            
    except Exception as e:
        st.error(f"資料讀取錯誤: {e}")
