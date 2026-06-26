import os
import yfinance as yf
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 1. 安全讀取 LINE Token
line_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

if not line_token:
    print("錯誤：缺少 LINE_CHANNEL_ACCESS_TOKEN，請檢查 GitHub Secrets 設定。")
    exit(1)

def send_line_with_retry(msg, token):
    """具備自動重試功能的發送函數"""
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    
    # 設定重試策略：自動重試 3 次，間隔 2 秒
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    
    return session.post(url, headers=headers, data={"message": msg})

def run_auto_monitor(ticker="2330.TW"):
    # 2. 抓取數據
    df = yf.download(ticker, period="1mo", progress=False)
    
    if df.empty:
        print(f"無法取得 {ticker} 的數據")
        return

    # 3. 計算技術指標
    sma_20 = df['Close'].rolling(window=20).mean().iloc[-1].item()
    last_price = df['Close'].iloc[-1].item()
    
    # 4. 判斷多空狀態
    status = "多頭趨勢 (價格高於均線)" if last_price > sma_20 else "空頭趨勢 (價格低於均線)"
    
    # 5. 製作監控報告
    msg = (
        f"\n【每日股價監控】\n"
        f"標的: {ticker}\n"
        f"最新價: {last_price:.2f}\n"
        f"20日均線: {sma_20:.2f}\n"
        f"目前狀態: {status}"
    )
    
    # 6. 呼叫具備重試機制的發送函數
    response = send_line_with_retry(msg, line_token)
    
    if response.status_code == 200:
        print(f"{ticker} 監控報告已成功發送至 LINE！")
    else:
        print(f"發送失敗，錯誤碼: {response.status_code}")

if __name__ == "__main__":
    run_auto_monitor("2330.TW")
