import os
from analysis_utils import get_stock_analysis
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

line_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

def run():
    # 您想監控的股票清單
    tickers = ["2330.TW", "2317.TW", "2454.TW"]
    
    report_lines = ["【每日股票監控報告】"]
    
    for t in tickers:
        price, sma, status, _ = get_stock_analysis(t)
        if price:
            report_lines.append(f"\n標的: {t}\n現價: {price:.2f} | 均線: {sma:.2f}\n狀態: {status}")
        else:
            report_lines.append(f"\n標的: {t} - 無法取得數據")
            
    # 將所有訊息合併為一則訊息發送
    msg = "\n".join(report_lines)
    
    # 發送邏輯 (同前，省略重複代碼)
    url = "https://notify-api.line.me/api/notify"
    requests.post(url, headers={"Authorization": f"Bearer {line_token}"}, data={"message": msg})

if __name__ == "__main__":
    run()
