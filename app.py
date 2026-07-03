import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="AI 專業金融分析終端")

def load_data():
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def render_table(info, key, title):
    """通用表格渲染器：確保格式固定"""
    data = info.get(key)
    if data and isinstance(data, list):
        try:
            df = pd.DataFrame(data)
            st.subheader(title)
            # 使用自動寬度並強制轉字串，確保不報錯
            st.dataframe(df.astype(str), use_container_width=True)
        except Exception as e:
            st.write(f"{title} 渲染錯誤: {e}")
    else:
        st.write(f"{title}: 暫無詳細數據")

def main():
    st.title("📊 AI 專業金融分析終端")
    data = load_data()
    
    # 選股介面
    with st.sidebar:
        st.header("選股控制台")
        ticker_input = st.text_input("輸入股票代號", "2330.TW")
        if st.button("確認選股"):
            st.session_state.target = ticker_input
            st.rerun()
            
    target = st.session_state.get("target", "2330.TW")
    info = data.get(target, {})

    # 1. 即時股價與選擇
    st.header(f"1. 即時股價: {target}")
    price = info.get("price", 0)
    diff = info.get("diff", 0)
    st.metric("當前價格", f"{price} 元", delta=f"{diff} 元")

    # 2. 基本面數據
    c1, c2, c3 = st.columns(3)
    c1.metric("每股淨值 (NAV)", "查詢中")
    c2.metric("本益比 (P/E)", info.get("pe", "N/A"))
    c3.metric("EPS", info.get("eps", "N/A"))

    # 4. 財務報表與預測 (置於新聞後)
    st.subheader("4. 財務與新聞分析")
    st.info(f"📰 GPT 新聞解讀: {info.get('news_analysis', '無即時新聞')}")
    st.success(f"🤖 AI 財報預測: {info.get('ai_prediction', '分析中...')}")

    # 5. 黑天鵝警示 (特別標記)
    st.subheader("⚠️ 黑天鵝危機警示")
    st.error(info.get("black_swan_alert", "系統監控中：無異常波動"))

    # 6. 法人與券商資料
    render_table(info, "institutional_daily", "5. 三大法人買賣超 (10日)")
    render_table(info, "broker_daily", "6. 10日資券比與主力券商")

if __name__ == "__main__":
    main()
