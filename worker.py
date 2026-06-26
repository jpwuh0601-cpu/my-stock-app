import os
import yfinance as yf
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 1. 取得環境變數
line_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

if not line_token:
    print("錯誤：缺少 LINE_CHANNEL_ACCESS_TOKEN")
    exit(1)

def send_line_with_retry(msg, token):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    
    # 建立一個 Session 並設定詳細的重試策略
    session = requests.Session()
    # 這裡加入連線超時與 DNS 解析失敗的處理
    retry_strategy = Retry(
        total=5,  # 增加總嘗試次數
        backoff_factor=2,  # 每次失敗等待時間加倍 (2s, 4s, 8s...)
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    
    try:
        # 增加 timeout 防止請求卡死
        response = session.post(url, headers=headers, data={"message": msg}, timeout=10)
        return response
    except requests.exceptions.RequestException as e:
        print(f"網路連線錯誤: {e}")
        return None

def run_auto_monitor(ticker="2330.TW"):
    # 2. 抓取數據
    df = yf.download(ticker, period="1mo", progress=False)
    
    if df.empty:
        print("無法取得數據")
        return

    # 3. 計算技術指標
    sma_20 = df['Close'].rolling(window=20).mean().iloc[-1].item()
    last_price = df['Close'].iloc[-1].item()
    status = "多頭趨勢 (價格高於均線)" if last_price > sma_20 else "空頭趨勢 (價格低於均線)"
    
    # 4. 製作監控報告
    msg = f"\n【每日股價監控】\n標的: {ticker}\n最新價: {last_price:.2f}\n20日均線: {sma_20:.2f}\n目前狀態: {status}"
    
    # 5. 發送 (加入了處理 None 的邏輯)
    response = send_line_with_retry(msg, line_token)
    
    if response and response.status_code == 200:
        print(f"{ticker} 報告已成功發送！")
    else:
        print("發送報告失敗，請檢查網路環境。")

if __name__ == "__main__":
    run_auto_monitor("2330.TW")
