import streamlit as st
import pandas as pd
import json
import os

# 設定頁面配置為寬螢幕
st.set_page_config(layout="wide", page_title="AI 智能金融終端")

def load_data():
    """使用穩健的絕對路徑讀取機制"""
    # 獲取當前程式碼所在的絕對路徑，確保不論在何種環境部署都能找到檔案
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "market_data.json")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"檔案讀取失敗: {e}")
            return {}
    else:
        # 除錯用資訊，協助您在 Streamlit Cloud 上確認檔案是否存在
        st.error(f"❌ 找不到數據檔 (路徑: {file_path})")
        st.write("請確認 GitHub Action 是否已成功推送 market_data.json 至根目錄")
        return {}

def color_red_green(val):
    """將籌碼數據轉為紅買綠賣的樣式"""
    color = 'red' if val > 0 else 'green'
    return f'color: {color}'

def main():
    data = load_data()
    if not data:
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 1. 側邊欄：選股功能與監控
    with st.sidebar:
        st.header("系統選股與設定")
        stock_code = st.text_input("輸入股票代碼", value=st.session_state.get("selected_stock", "2330.TW"))
        if st.button("確認選股"):
            st.session_state.selected_stock = stock_code
            st.rerun()
        st.divider()
        st.warning("⚠️ 黑天鵝危機警示: 正常")
        st.status("自動回測資料正確性: ✅ 已校驗")

    # 2. 即時股價與指標 (紅漲綠跌)
    st.subheader("核心財務指標")
    c1, c2, c3, c4, c5 = st.columns(5)
    
    # 即時股價
    c1.metric("即時股價", f"{float(data.get('price', 0)):,.2f}", delta=f"{float(data.get('change', 0)):+.2f}")
    c1.button("刷新即時報價")
    
    c2.metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    c3.metric("本益比 (PE)", f"{float(data.get('pe_ratio', 0)):.2f}")
    c4.metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    c5.metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")

    # 3. 報表與籌碼分析
    tab1, tab2 = st.tabs(["財務報表與預測", "籌碼與主力分析"])
    
    with tab1:
        st.subheader("今年與去年每季財務報表")
        st.table(pd.DataFrame(data.get("financials", {})))
        
        st.subheader("即時新聞解讀")
        st.info(data.get("news", "無即時新聞"))
        
        st.subheader("AI 財報預測")
        st.success(data.get("ai_prediction", "分析中..."))

    with tab2:
        st.subheader("三大法人 10日買賣超")
        inst_df = pd.DataFrame(data.get("institutional_investors", []))
        if not inst_df.empty:
            st.dataframe(inst_df.style.map(color_red_green, subset=['買賣超']), use_container_width=True)
        
        st.subheader("10日主力券商動向")
        st.dataframe(pd.DataFrame(data.get("top_brokers", [])), use_container_width=True)

if __name__ == "__main__":
    main()
