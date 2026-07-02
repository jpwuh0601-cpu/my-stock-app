import streamlit as st
import pandas as pd
import json
import os

# 設定頁面樣式
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """讀取市場數據，若失敗則回傳空字典"""
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"讀取資料檔時發生錯誤: {e}")
            return {}
    return {}

def main():
    data = load_data()
    
    if not data:
        st.info("尚未載入數據，請等待 GitHub Actions 下次更新或手動觸發...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標：顯示防護層
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    cols[1].metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    cols[2].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[3].metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    cols[4].metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    # 籌碼面：顯示防護層
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors")
    
    if isinstance(inst_data, list) and len(inst_data) > 0:
        # 將資料轉換為易讀的 DataFrame
        df = pd.DataFrame(inst_data)
        st.dataframe(df, width=1000)
    else:
        st.warning("目前無法人籌碼數據。")

    # AI 分析與新聞
    st.subheader("AI 智能分析與市場新聞")
    st.info(data.get("ai_prediction", "暫無 AI 分析結果。"))
    st.write(data.get("news", "暫無新聞數據。"))

if __name__ == "__main__":
    main()
