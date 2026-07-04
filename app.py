import streamlit as st
import json
import os
import pandas as pd

# 頁面配置
st.set_page_config(layout="wide", page_title="專業金融監控終端")

def load_data(filepath):
    if not os.path.exists(filepath): return {}
    with open(filepath, "r", encoding="utf-8") as f: return json.load(f)

# 設定紅綠漲跌樣式
def color_negative_red(val):
    color = 'red' if val > 0 else 'green'
    return f'color: {color}'

def main():
    st.title("📈 專業金融監控終端")
    data = load_data("market_data.json")
    
    # 1. 側邊欄：選股
    with st.sidebar:
        ticker = st.selectbox("選擇監控標的", list(data.keys()))
        if st.button("確認選股"):
            st.session_state.target = ticker
            st.rerun()

    target = st.session_state.get("target", "2330.TW")
    info = data.get(target, {})

    # 2. 即時股價 (漲紅跌綠)
    price = info.get("price", 0)
    change = info.get("change", 0)
    delta_color = "normal" if change == 0 else ("inverse" if change > 0 else "normal")
    st.metric("即時股價", f"{price} 元", delta=f"{change} 元")

    # 3. 財務基礎指標
    st.subheader("基本面指標")
    c1, c2, c3 = st.columns(3)
    c1.metric("每股淨值", info.get("nav", "N/A"))
    c2.metric("本益比", info.get("pe", "N/A"))
    c3.metric("EPS", info.get("eps", "N/A"))

    # 4. 財報預測 (放在即時新聞後)
    st.subheader("🤖 AI 財報預測")
    st.info(info.get("ai_prediction", "分析中..."))

    # 5. 三大法人 10 日買賣超 (紅賣綠買)
    st.subheader("三大法人 10 日買賣超")
    if "institutional_data" in info:
        df_inst = pd.DataFrame(info["institutional_data"])
        st.dataframe(df_inst.style.map(color_negative_red, subset=['買賣超']))

    # 6. 資券比與主力券商
    st.subheader("10 日資券比與主力動向")
    c_a, c_b = st.columns(2)
    c_a.metric("資券比", f"{info.get('margin_ratio', 0)}%")
    c_b.write(f"主力券商: {info.get('top_broker', '分析中')}")

    # 7. 營收預測與股利
    st.subheader("年度預估財務數據")
    st.table(pd.DataFrame({
        "預估項目": ["年度營收", "年度 EPS", "預估股利"],
        "數值": [info.get("est_revenue", "N/A"), info.get("est_eps", "N/A"), info.get("est_dividend", "N/A")]
    }))

if __name__ == "__main__":
    main()
