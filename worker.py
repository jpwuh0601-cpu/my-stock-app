import requests
import yfinance as yf
from bs4 import BeautifulSoup

def fetch_stock_data(ticker_symbol):
    """
    從 Yahoo Finance 抓取股價等基本資料，加入資料完整性檢查
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        # 確保必要的欄位存在，否則給予預設值
        return {
            "price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
            "marketCap": info.get("marketCap", 0)
        }
    except Exception as e:
        print(f"fetch_stock_data 錯誤: {e}")
        # 回傳預設值而非 None，避免 main_task 邏輯崩潰
        return {"price": 0, "marketCap": 0}

def fetch_real_broker_data(ticker_symbol):
    """
    獲取真實券商分點明細，優化異常回傳結構
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
        
        # 若爬取到空列表，回傳結構化的預設值，避免下游處理報錯
        return data if data else [{"券商": "無資料", "買賣張數": "0"}]
        
    except Exception as e:
        print(f"fetch_real_broker_data 錯誤: {e}")
        return [{"券商": "錯誤", "買賣張數": "0"}]

# 確保這兩個函數都被定義了，這樣 main_task.py 才能正確 import
