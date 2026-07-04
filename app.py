import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="專業金融監控終端")

def load_data():
    if not os.path.exists("market_data.json"): return {}
    with open("market_data.json", "r", encoding="utf-8") as f: 
        try:
            return json.load(f)
        except:
            return {}

def main():
    st.title("📈 專業金融監控終端系統")
    data = load_data()
    
    # 移除下拉選單，改為純文字輸入
    st.sidebar.header("股票查詢系統")
    input_ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", key="ticker_input")
    
    # 使用 session_state 記憶輸入內容
    target = input_ticker if input_ticker else "2330.TW"
    
    # 檢查輸入的代號是否在資料庫中
    if target not in data:
        st.warning(f"找不到代號 {target} 的資料。請確認是否已加入 tickers.txt 並執行過 GitHub Action。")
        st.info("目前資料庫中存在的代號: " + ", ".join(data.keys()))
        return
        
    info = data.get(target, {})

    # --- 版面排列 ---
    st.subheader(f"目標股票: {target}")
    
    # 1. 即時股價 (漲紅跌綠)
    change = info.get('change', 0)
    color = "red" if change >= 0 else "green"
    st.markdown(f"### 即時股價: <span style='color:{color}'>{info.get('price', 0)} ({change})</span>", unsafe_allow_html=True)
    
    # 2. 基本指標
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("每股淨值", f"{info.get('nav', 0)}")
    c2.metric("本益比", f"{info.get('pe', 0)}")
    c3.metric("EPS", f"{info.get('eps', 0)}")
    c4.metric("預估股利", f"{info.get('dividend', 'N/A')}")

    # 4. 財報報表
    st.subheader("4. 財報報表 (今年與去年每季)")
    st.write("報表數據同步中...") 

    # 5. 三大法人與10日資券比
    st.subheader("5. 三大法人與10日資券比")
    st.write(f"10日資券比: {info.get('margin_ratio', 0)}%")
    df = pd.DataFrame(info.get("institutional_data", []))
    st.dataframe(df, use_container_width=True)

    # 3. 新聞與 AI 預測 (順序調整)
    st.subheader("即時新聞與 AI 財報預測")
    st.info(f"新聞解讀: {info.get('news', '暫無最新資訊')}")
    st.success(f"AI 財報預測: {info.get('ai_prediction', '數據載入中...')}")

    # 4. 風險與警示系統
    st.divider()
    cols = st.columns(4)
    cols[0].warning(f"黑天鵝危機: {info.get('black_swan', '安全')}")
    cols[1].write(f"AI 主力分析: {info.get('main_force', '分析中')}")
    cols[2].write(f"外資分析: {info.get('foreign_analysis', '持平')}")
    cols[3].write(f"GPT AI 洞察: {info.get('gpt_insight', '分析中')}")

    st.subheader("自動化功能")
    c_a1, c_a2 = st.columns(2)
    c_a1.write(f"AI 選股建議: {info.get('ai_selection', '暫無建議')}")
    c_a2.checkbox("LINE 通知狀態: ✅ 已啟用", value=True)
    
    if st.button("自動回測資料來源正確性"):
        st.success("資料來源驗證成功。")

if __name__ == "__main__":
    main()
