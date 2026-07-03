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

def color_df(val):
    """紅漲綠跌視覺化邏輯"""
    try:
        # 將數值轉為浮點數進行比較
        num = float(str(val).replace(',', ''))
        color = 'red' if num > 0 else ('green' if num < 0 else 'black')
        return f'color: {color}'
    except:
        return ''

def render_styled_table(data_key, info, title):
    """渲染帶有顏色樣式的表格"""
    raw_data = info.get(data_key)
    if raw_data:
        try:
            df = pd.DataFrame(raw_data)
            st.subheader(title)
            # 應用顏色格式化
            styled_df = df.style.applymap(color_df)
            st.dataframe(styled_df, use_container_width=True)
        except Exception as e:
            st.warning(f"無法繪製表格: {e}")
    else:
        st.write(f"{title}: 暫無詳細細項資料")

def main():
    st.title("📈 AI 專業金融分析終端")
    data = load_data()
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    with st.sidebar:
        target = st.selectbox("請選擇股票", tickers)
        if st.button("確定選股"):
            st.session_state.target = target
            
    sym = st.session_state.get("target", tickers[0] if tickers else "")
    info = data.get(sym, {})

    # 1. 即時股價與漲跌價錢
    price = info.get("price", 0)
    prev = info.get("prev_close", 0)
    diff = round(price - prev, 2)
    delta_color = "normal" if diff == 0 else ("inverse" if diff > 0 else "normal")
    
    st.header(f"股票: {sym}")
    st.metric("即時股價", f"{price} 元", delta=f"{diff} 元")

    # 5. 三大法人買賣超 (每日細項)
    render_styled_table("institutional_daily", info, "5. 三大法人 10 日買賣超細項")

    # 6. 主力券商買賣超 (每日細項)
    render_styled_table("broker_daily", info, "6. 主力券商 10 日買賣超細項")

    # 7. AI 分析
    st.subheader("7. AI 財報與風險分析")
    st.success(info.get("ai_prediction", "分析中..."))

if __name__ == "__main__":
    main()
