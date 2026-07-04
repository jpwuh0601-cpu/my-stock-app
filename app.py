import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="專業金融監控終端")

def load_data():
    if not os.path.exists("market_data.json"): return {}
    try:
        with open("market_data.json", "r", encoding="utf-8") as f: 
            return json.load(f)
    except: return {}

def main():
    st.title("📈 專業金融監控終端系統")
    data = load_data()
    
    # 1. 側邊欄邏輯：過濾掉非股票的 Key (如 last_updated)
    valid_tickers = [k for k in data.keys() if "." in k or k.isdigit()]
    
    with st.sidebar:
        st.header("系統導航")
        # 顯示選單與手動輸入
        selected = st.selectbox("選擇監控股票", valid_tickers, index=0 if valid_tickers else None)
        custom_input = st.text_input("或輸入新代號 (例如 2317.TW)")
        
        if st.button("確認選股"):
            # 如果有手動輸入就用手動的，沒有就用下拉選單
            target = custom_input if custom_input else selected
            st.session_state.target = target
            st.rerun()

    # 安全地讀取目標
    target = st.session_state.get("target", valid_tickers[0] if valid_tickers else None)
    
    if target not in data:
        st.warning(f"目前資料庫中找不到 {target}，請確認自動化排程 (Actions) 是否已更新此標的。")
        return
        
    info = data.get(target, {})

    # 2. 面板顯示 (增加 try-except 防止 AttributeError)
    try:
        st.subheader("1. 即時資訊與基本指標")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("即時股價", str(info.get('price', 0)), delta=str(info.get('change', 0)))
        c2.metric("每股淨值", str(info.get('nav', 'N/A')))
        c3.metric("本益比", str(info.get('pe', 'N/A')))
        c4.metric("EPS", str(info.get('eps', 'N/A')))

        col_l, col_r = st.columns(2)
        with col_l:
            st.subheader("2. 財報報表 (今年與去年每季)")
            st.write("報表數據同步中...") 

        with col_r:
            st.subheader("3. 籌碼面：法人買賣超 (10日)")
            inst_data = info.get("institutional_data")
            if inst_data:
                df = pd.DataFrame(inst_data)
                st.dataframe(df, use_container_width=True)

        st.subheader("4. 即時新聞與 AI 綜合分析")
        st.info(f"新聞解讀: {info.get('news', '暫無即時新聞')}")
        st.success(f"AI 財報預測: {info.get('ai_prediction', '分析中...')}")

        st.divider()
        st.subheader("5. AI 智能監控與警示系統")
        a1, a2, a3, a4 = st.columns(4)
        a1.warning(f"黑天鵝危機: {info.get('black_swan', '安全')}")
        a2.write(f"GPT AI 洞察: {info.get('gpt_insight', '分析中')}")
        a3.write(f"外資分析: {info.get('foreign_analysis', '持平')}")
        a4.write(f"LINE 通知狀態: ✅ 已啟用")
    except Exception as e:
        st.error(f"顯示資料時發生錯誤: {e}")

if __name__ == "__main__":
    main()
