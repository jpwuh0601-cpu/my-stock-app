import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

# 設定頁面風格
st.set_page_config(layout="wide", page_title="金融智慧監控終端")

def main():
    st.title("📈 專業金融智慧監控系統")
    
    # 讀取數據檔案
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                st.error("資料檔案讀取異常，請檢查自動化任務執行狀態。")
                return
    else:
        st.warning("尚未偵測到數據，請等待 GitHub Actions 更新...")
        return

    # 1. 全域風險偵測看板 (自動標示所有高風險股票)
    risky_stocks = [symbol for symbol, info in data.items() if info.get('black_swan') == "⚠️ 高風險警示"]
    if risky_stocks:
        st.error(f"🚨 **全局風險警報**：以下標的觸發黑天鵝風險 - {', '.join(risky_stocks)}")

    # 2. 側邊欄：股票選擇器
    target = st.sidebar.selectbox("選擇監控標的", list(data.keys()))
    
    if target in data:
        info = data[target]
        
        # 標題與警示狀態
        st.header(f"標的分析: {target}")
        if info.get('black_swan') == "⚠️ 高風險警示":
            st.error("狀態: ⚠️ 高風險警示 (建議減碼)")
        else:
            st.success("狀態: ✅ 運作安全")
            
        # 指標卡片顯示
        col1, col2, col3 = st.columns(3)
        col1.metric("即時價格", f"{info.get('price', 0)}")
        col2.metric("EPS (每股盈餘)", info.get('eps', 0))
        col3.metric("本益比 (PE)", info.get('pe', 0))
        
        # 3. 籌碼視覺化
        st.subheader("📊 三大法人籌碼趨勢")
        inst_data = info.get('institutional_data', [])
        if inst_data:
            df_inst = pd.DataFrame(inst_data)
            df_melt = df_inst.melt(id_vars="日期", var_name="法人", value_name="買賣超")
            fig = px.bar(df_melt, x="日期", y="買賣超", color="法人", barmode="group",
                         title="法人近 3 日買賣超分佈")
            st.plotly_chart(fig, use_container_width=True)
            
        # 4. AI 輿情分析
        st.subheader("🤖 AI 市場觀點")
        with st.expander("展開 AI 深度解讀"):
            st.write(f"**最新新聞:** {info.get('news', '無')}")
            st.info(f"**AI 情緒分析:** {info.get('ai_prediction', '分析中...')}")
    else:
        st.write("查無此標的數據。")

if __name__ == "__main__":
    main()
