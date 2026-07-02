import streamlit as st
import pandas as pd
import json
import os

# 設定頁面配置
st.set_page_config(layout="wide", page_title="AI 智能金融終端")

def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

# 紅買綠賣邏輯 (用於籌碼表格)
def color_red_green(val):
    color = 'red' if val > 0 else 'green'
    return f'color: {color}'

def main():
    data = load_data()
    
    # --- 1. 側邊欄選股 ---
    with st.sidebar:
        st.header("選股設定")
        stock_code = st.text_input("輸入股票代碼", value="2330.TW")
        if st.button("確認選股"):
            st.session_state.selected_stock = stock_code
            st.rerun() # 點擊後重新載入以更新數據
        
        st.write(f"目前監控中: {st.session_state.get('selected_stock', '2330.TW')}")

    # --- 2. 頂部即時股價 (紅漲綠跌) ---
    st.title("📈 AI 智能金融監控終端")
    
    price = float(data.get("price", 0))
    change = float(data.get("change", 0))
    
    # metric 的 delta 正數會自動變紅，負數自動變綠
    st.metric("即時股價", f"{price:,.2f}", delta=f"{change:+.2f}")
    
    st.divider()

    # --- 3. 三大法人 10 日買賣超 (紅賣綠賣格式化) ---
    st.subheader("三大法人 10日買賣超")
    inst_data = data.get("institutional_investors", [])
    if inst_data:
        df_inst = pd.DataFrame(inst_data)
        # 這裡將「買賣超」欄位套用顏色邏輯
        styled_df = df_inst.style.map(color_red_green, subset=['買賣超'])
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.info("暫無三大法人數據")

if __name__ == "__main__":
    main()
