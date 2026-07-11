import streamlit as st

# 1. 最精簡的頁面載入測試
st.title("環境運作測試")
st.write("如果看到這行字，代表前端與後端已經成功連線！")

# 2. 測試最簡單的輸入互動
ticker = st.text_input("輸入代號", "2330")

if st.button("確認"):
    st.write(f"系統已成功接收到輸入：{ticker}")

# 3. 如果這行字出現，代表系統完全正常
st.success("環境運作一切正常，可以開始增加功能了。")
