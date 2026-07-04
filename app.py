import streamlit as st
import pandas as pd
import json
import os

# 1. 頁面優化：設定簡約佈局以降低載入負擔
st.set_page_config(page_title="金融儀表板", layout="centered")

def load_data(filepath):
    """防禦性讀取 JSON"""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def main():
    st.title("📈 金融分析終端")
    
    data = load_data("market_data.json")
    target = st.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
    
    info = data.get(target)
    
    if not info:
        st.info("資料載入中... 若無回應，請檢查 GitHub Actions 是否已執行完成。")
        return

    # 顯示數據
    st.metric("即時股價", f"{info.get('price', 0)} 元")
    
    # 使用 width=None 取代 use_container_width=True 以符合新規範
    if "institutional_daily" in info:
        st.subheader("法人籌碼")
        st.dataframe(pd.DataFrame(info["institutional_daily"]), width=None)

    st.success(f"🤖 AI 預測: {info.get('ai_prediction', '分析中...')}")

if __name__ == "__main__":
    main()
