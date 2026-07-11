import streamlit as st

st.title("穩定版測試")
st.write("如果看到這行字，代表伺服器與渲染引擎已恢復正常！")

# 模擬一個簡單的互動，確認輸入框功能正常
ticker = st.text_input("輸入代號", "2330")
if st.button("確認"):
    st.success(f"系統已成功接收到輸入：{ticker}")
