import requests
import streamlit as st

def send_line_notify(message, ticker=None):
    """
    發送 LINE 通知，並附帶看板連結與正確的格式處理
    """
    # 從 Streamlit Secrets 取得 Token
    token = st.secrets.get("LINE_CHANNEL_ACCESS_TOKEN")
    if not token:
        print("警告: LINE_CHANNEL_ACCESS_TOKEN 未設定，無法發送通知。")
        return
    
    # 您的 Streamlit App 線上網址
    url_base = "https://my-stock-app-m32nrnf56v5bzxaqcxr9xy.streamlit.app"
    
    # 建構訊息內容
    # 若有指定股票，可顯示特定路徑，若無則顯示首頁
    target_url = f"{url_base}/?ticker={ticker}" if ticker else url_base
    
    full_message = f"\n📊 AI 股市分析通知\n\n{message}\n\n🔗 點擊查看詳細籌碼分析:\n{target_url}"
    
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(
            url, 
            headers=headers, 
            data={"message": full_message}, 
            timeout=10
        )
        response.raise_for_status()
        print(f"LINE 通知發送成功: {ticker if ticker else 'General'}")
    except Exception as e:
        print(f"LINE 通知發送失敗: {e}")

# 測試用區塊：若直接執行此檔可測試發送
if __name__ == "__main__":
    send_line_notify("這是一則測試訊息，系統運作正常。", "2330.TW")
