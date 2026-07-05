import requests
import streamlit as st

def send_line_notify(message):
    """發送訊息至 LINE，並增強錯誤處理機制以避免影響主程式穩定性"""
    try:
        # 使用 get 方法防止 KeyMissing 錯誤
        token = st.secrets.get("LINE_CHANNEL_ACCESS_TOKEN")
        
        if not token:
            print("警告：未在 Streamlit Secrets 中找到 LINE_CHANNEL_ACCESS_TOKEN。")
            return
        
        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {token}"}
        data = {"message": message}
        
        # 增加 timeout 設定，避免因網路延遲導致主程式卡死
        response = requests.post(url, headers=headers, data=data, timeout=10)
        
        if response.status_code == 200:
            print("LINE 通知發送成功！")
        else:
            print(f"LINE 通知發送失敗，HTTP 錯誤碼: {response.status_code}, 內容: {response.text}")
            
    except requests.exceptions.Timeout:
        print("發送 LINE 通知超時，請檢查網路連接。")
    except Exception as e:
        print(f"發送 LINE 通知時發生未預期的錯誤: {str(e)}")
