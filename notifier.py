import requests
import os

def send_line_notify(message, ticker=None):
    """支援 Streamlit Secrets 與 GitHub 環境變數的通知發送器"""
    
    # 優先從環境變數讀取 (GitHub Actions 使用)，否則從 streamlit.secrets 讀取
    token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    if not token:
        try:
            import streamlit as st
            token = st.secrets.get("LINE_CHANNEL_ACCESS_TOKEN")
        except ImportError:
            pass
            
    if not token:
        print("警告: 找不到 LINE_CHANNEL_ACCESS_TOKEN，請確保已設定環境變數或 Secrets")
        return
    
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    
    # 構建訊息內容
    full_message = f"\n📊 AI 股市分析通知\n\n{message}"
    
    try:
        response = requests.post(url, headers=headers, data={"message": full_message}, timeout=10)
        response.raise_for_status()
        print("LINE 通知發送成功")
    except Exception as e:
        print(f"LINE 通知發送失敗: {e}")
