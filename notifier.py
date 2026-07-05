import requests
import os

def send_line_notify(message):
    """發送訊息至 LINE"""
    token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    if not token:
        print("未設定 LINE_CHANNEL_ACCESS_TOKEN，跳過通知。")
        return
    
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": message}
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print("LINE 通知發送成功！")
    else:
        print(f"LINE 通知發送失敗，錯誤碼: {response.status_code}")
