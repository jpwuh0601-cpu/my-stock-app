import requests
import os

def send_line_notify(message):
    """
    修正版通知發送器：完全依賴環境變數，避免讀取 Streamlit Secrets 失敗
    """
    # 直接從環境變數讀取
    token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    
    if not token:
        print("錯誤: 無法讀取 LINE_CHANNEL_ACCESS_TOKEN，請確認 GitHub Secrets 設定")
        return
    
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(url, headers=headers, data={"message": f"\n📊 {message}"}, timeout=10)
        response.raise_for_status()
        print("LINE 通知發送成功")
    except Exception as e:
        print(f"LINE 通知發送失敗: {e}")

if __name__ == "__main__":
    send_line_notify("系統已完成資料更新測試。")
