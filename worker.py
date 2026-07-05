import requests
from bs4 import BeautifulSoup

def fetch_real_broker_data(ticker_symbol):
    """
    獲取真實券商分點明細 (Goodinfo 範例)
    """
    try:
        # 移除 .TW 以符合網址格式
        code = ticker_symbol.split('.')[0]
        url = f"https://goodinfo.tw/tw/StockBroker.asp?STOCK_ID={code}"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根據 Goodinfo 結構抓取表格
        # 注意：若網頁改版，可能需要調整這裡的 CSS Selector
        table = soup.find('table', {'id': 'tblStockBroker'})
        data = []
        if table:
            rows = table.find_all('tr', {'class': 'bg_white'})
            for row in rows[:5]: # 取前 5 大分點
                cols = row.find_all('td')
                if len(cols) > 2:
                    broker_name = cols[0].text.strip()
                    buy_sell = cols[1].text.strip()
                    data.append({"券商": broker_name, "買賣張數": buy_sell})
        return data
    except Exception as e:
        print(f"真實券商爬蟲執行中斷: {e}")
        return [{"日期": "Error", "券商": "暫無數據", "買賣張數": 0}]
