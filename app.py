import streamlit as st
import json

# 設定頁面配置
st.set_page_config(page_title="股市儀表板", layout="wide")

st.title("📈 股市決策儀表板")

# 讀取數據
try:
    with open("market_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except:
    data = {}

# 股票選擇
ticker = st.selectbox("請選擇股票", list(data.keys()) if data else ["請先執行 main_task.py"])

if ticker in data:
    d = data[ticker]
    
    # 並排顯示核心指標
    st.markdown("### 核心指標")
    cols = st.columns(5)
    cols[0].metric("股價", d.get("price", 0))
    cols[1].metric("每股淨值", d.get("nav", 0))
    cols[2].metric("本益比", d.get("pe", 0))
    cols[3].metric("EPS", d.get("eps", 0))
    
    # 預估財務模型區塊
    st.markdown("---")
    st.subheader("📊 財務預估模型")
    
    # 參數設定
    c1, c2 = st.columns(2)
    margin_ratio = c1.slider("假設稅後淨利率 (%)", 5.0, 30.0, 15.0) / 100
    payout_ratio = c2.slider("假設盈餘分配率 (%)", 30.0, 90.0, 60.0) / 100
    
    # 計算邏輯 (假設成長率為 12% 如數據所示)
    est_revenue = d.get("last_year_revenue", 1e9) * 1.12
    est_net_profit = est_revenue * margin_ratio
    est_eps = est_net_profit / d.get("shares", 1e9)
    est_dividend = est_eps * payout_ratio
    
    # 並排顯示預估結果
    p_cols = st.columns(4)
    p_cols[0].metric("預估明年營收", f"{est_revenue/1e8:.1f} 億")
    p_cols[1].metric("預估稅後淨利", f"{est_net_profit/1e8:.1f} 億")
    p_cols[2].metric("預估 EPS", f"{est_eps:.2f}")
    p_cols[3].metric("預估現金股利", f"{est_dividend:.2f}")
    
    st.write("數據來源: market_data.json")
else:
    st.write("等待數據更新...")
