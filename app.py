import streamlit as st
import json
import os
import sys

# 頁面配置
st.set_page_config(page_title="股市儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 環境檢測與資料讀取
st.sidebar.write(f"Python 版本: {sys.version.split()[0]}")

try:
    with open("market_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    ticker = st.selectbox("請選擇股票", list(data.keys()))
    if ticker:
        d = data[ticker]
        # 顯示核心指標
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("股價", d.get("price", 0))
        col2.metric("每股淨值", d.get("nav", 0))
        col3.metric("本益比", d.get("pe", 0))
        col4.metric("EPS", d.get("eps", 0))
        
        # 第 9 項：財務預估面板
        st.markdown("---")
        st.subheader("📊 第 9 項：明年財務預估模型")
        
        # 參數調節器
        c1, c2 = st.columns(2)
        margin_rate = c1.slider("假設稅後淨利率 (%)", 5.0, 30.0, 15.0) / 100
        payout_rate = c2.slider("假設盈餘分配率 (%)", 30.0, 90.0, 60.0) / 100
        
        # 計算邏輯
        # 預估營收 = 去年營收 * (1 + 成長率)
        est_revenue = d.get("last_year_revenue", 1e9) * 1.12 
        est_net_profit = est_revenue * margin_rate
        est_eps = est_net_profit / d.get("shares", 1e9)
        est_dividend = est_eps * payout_rate
        
        # 並排顯示預估結果
        p1, p2, p3, p4 = st.columns(4)
        p1.metric("預估明年營收", f"{est_revenue/1e8:.1f} 億")
        p2.metric("預估稅後淨利", f"{est_net_profit/1e8:.1f} 億")
        p3.metric("預估 EPS", f"{est_eps:.2f}")
        p4.metric("預估現金股利", f"{est_dividend:.2f}")
        
        st.write("已成功載入數據與財務模型。")

except Exception as e:
    st.error(f"系統錯誤: {e}")
    st.info("若錯誤顯示為 module not found，請刪除 App 後重新部署，並確保 requirements.txt 檔案名稱正確無誤。")
