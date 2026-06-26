import os
import requests
from analysis_utils import get_stock_analysis
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

line_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

def send_line_with_retry(msg, token):
    url = "https://notify-api.line.me/api/notify"
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session.post(url, headers={"Authorization": f"Bearer {token}"}, data={"message": msg}, timeout=10)

def run():
    ticker = "2330.TW"
    price, sma, status = get_stock_analysis(ticker)
    
    if price:
        msg = f"\n【每日股價監控】\n標的: {ticker}\n最新價: {price:.2f}\n20日均線: {sma:.2f}\n目前狀態: {status}"
        send_line_with_retry(msg, line_token)

if __name__ == "__main__":
    run()
