import requests
import streamlit as st

def send_line_notify(message):
    """發送訊息至 LINE"""
    # 從 Streamlit Secrets 讀取 Token，這是確保在雲端部署時能安全獲取密鑰的正確方式
    try:
        # 請確保您的 Streamlit Cloud 設定中已加入 LINE_CHANNEL_ACCESS_TOKEN
        token = st.secrets.get("LINE_CHANNEL_ACCESS_TOKEN")
        
        if not token:
            print("警告：未在 Streamlit Secrets 中找到 LINE_CHANNEL_ACCESS_TOKEN。")
            return
        
        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {token}"}
        data = {"message": message}
        
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200:
            print("LINE 通知發送成功！")
        else:
            print(f"LINE 通知發送失敗，HTTP 錯誤碼: {response.status_code}, 內容: {response.text}")
            
    except Exception as e:
        print(f"發送 LINE 通知時發生未預期的錯誤: {str(e)}")
