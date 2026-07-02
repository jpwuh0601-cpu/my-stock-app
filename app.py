import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.set_page_config(layout="wide", page_title="AI 智能金融終端")
    
    # 1. 頂部即時監控
    with st.container():
        cols = st.columns([1, 1, 1, 1, 2])
        cols[0].metric("即時股價", "2,460.00", delta="+15.00") # 漲紅跌綠
        cols[1].metric("每股淨值", "150.20")
        cols[2].metric("融資券比", "1.25%")
        cols[3].metric("預估 EPS", "73.65")
        
    st.divider()

    # 2. 財報與營收區塊 (Grid Layout)
    tab1, tab2 = st.tabs(["財務報表", "籌碼面分析"])
    
    with tab1:
        st.subheader("財務數據 (今年/去年每季)")
        # 顯示營收、EPS、股利表格
        st.table(pd.DataFrame({"Q1": [10, 5], "Q2": [12, 6]}, index=["營收", "EPS"]))
        
        st.subheader("AI 財報預測")
        st.text("根據目前營收趨勢，預估今年度 EPS 為...")

    with tab2:
        # 3. 籌碼面：三大法人與主力券商 10 日
        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("三大法人 10日買賣超")
            # 這裡需要一個根據數值自動變色的表格函數
        with col_right:
            st.subheader("10日資券比與主力券商")
            
    # 4. AI 與深度分析 (置於新聞後)
    st.subheader("即時新聞與 AI 解讀")
    st.info("新聞標題...")
    st.success("AI 深度解讀: ...")

    # 5. 風險與系統監控 (底部)
    with st.sidebar:
        st.header("系統監控中心")
        st.warning("⚠️ 黑天鵝警示: 正常")
        st.status("自動回測資料來源: ✅ 已完成校驗")
        st.button("執行 LINE 通知")

if __name__ == "__main__":
    main()
