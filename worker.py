import requests
import yfinance as yf
from bs4 import BeautifulSoup

def fetch_stock_data(ticker_symbol):
    """
    從 Yahoo Finance 抓取股價等基本資料
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        return {
            "price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
            "marketCap": info.get("marketCap", 0)
        }
    except Exception as e:
        print(f"fetch_stock_data 錯誤: {e}")
        return None

def fetch_real_broker_data(ticker_symbol):
    """
    獲取真實券商分點明細
    """
    try:
        code = str(ticker_symbol).split('.')[0].strip()
        url = f"https://goodinfo.tw/tw/StockBroker.asp?STOCK_ID={code}"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('table', {'id': 'tblStockBroker'})
        data = []
        if table:
            rows = table.find_all('tr', {'class': 'bg_white'})
            for row in rows[:5]:
                cols = row.find_all('td')
                if len(cols) > 2:
                    broker_name = cols[0].text.strip()
                    buy_sell = cols[1].text.strip()
                    data.append({"券商": broker_name, "買賣張數": buy_sell})
        return data
    except Exception as e:
        print(f"fetch_real_broker_data 錯誤: {e}")
        return [{"日期": "Error", "券商": "暫無數據", "買賣張數": 0}]

# 確保這兩個函數都被定義了，這樣 main_task.py 才能正確 import
