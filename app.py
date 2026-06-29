import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="專業投資決策儀表板", layout="wide")

st.title("📈 專業投資決策儀表板")

def load_and_validate_data():
    """載入並回測資料來源是否正確"""
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # 簡單回測：檢查必要的關鍵欄位是否存在
            required_keys = ['price', 'bvps', 'financials', 'institutional_investors']
            for key in required_keys:
                if key not in data:
                    st.error(f"資料錯誤：缺少關鍵欄位 '{key}'，請檢查 worker.py 輸出")
                    return None
            return data
    except Exception as e:
        st.error(f"無法讀取數據：{e}")
        return None

data = load_and_validate_data()

if data:
    update_date = data.get('update_date', '未知日期')
    st.caption(f"最後更新時間: {update_date}")

    # 1 & 2. 即時股價與每股淨值
    col1, col2 = st.columns(2)
    col1.metric("即時股價", f"${data.get('price', 0)}")
    col2.metric("每股淨值 (BVPS)", f"${data.get('bvps', 0)}")

    st.divider()

    tab1, tab2, tab3 = st.tabs(["財務與績效", "籌碼面分析", "AI 預測與市場動態"])

    with tab1:
        # 4. 今年與去年每季報表
        st.subheader("每季財務報表 (去年至今年)")
        st.table(pd.DataFrame(data.get('financials', {})))
        
        # 預估今年營收、EPS 與股利
        st.subheader("年度財務預估")
        f_col1, f_col2, f_col3 = st.columns(3)
        f_col1.metric("預估今年營收", f"{data.get('est_revenue', 'N/A')}")
        f_col2.metric("預估 EPS", f"{data.get('est_eps', 'N/A')}")
        f_col3.metric("預估股利", f"{data.get('est_dividend', 'N/A')}")

    with tab2:
        # 5. 三大法人與券商自營商
        st.subheader("三大法人買賣超 (近10日)")
        df_inst = pd.DataFrame(data.get('institutional_investors', []))
        
        def color_map(val):
            return f'color: {"red" if val > 0 else "green"}'
        
        if not df_inst.empty:
            st.dataframe(df_inst.style.applymap(color_map, subset=['買賣超']), use_container_width=True)
        
        # 6. 10日資券比與主力券商
        st.subheader("籌碼面統計")
        col_a, col_b = st.columns(2)
        col_a.metric("10日資券比", f"{data.get('margin_ratio', 0)}%")
        
        st.subheader("主力券商與自營商買賣統計")
        st.json(data.get('top_brokers', {}))

    with tab3:
        # 7. 最新新聞與 AI 財報預測 (調整順序)
        st.subheader("最新市場新聞")
        for news in data.get('news', []):
            st.write(f"• {news}")
            
        st.subheader("AI 財報預測")
        st.info(data.get('ai_prediction', '無預測數據'))

else:
    st.warning("數據源尚未準備就緒或檢核失敗，請等待自動化排程更新...")
