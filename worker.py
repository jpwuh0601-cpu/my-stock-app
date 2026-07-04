import yfinance as yf
import json

def get_ai_analysis(ticker_symbol):
    """
    負責抓取股票數據並進行分析的模組
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        
        # 獲取基礎數據
        data = {
            "price": info.get('currentPrice', 0),
            "eps": info.get('trailingEps', 0),
            "pe": info.get('forwardPE', 0),
            "ai_prediction": f"基於最新 EPS {info.get('trailingEps', 'N/A')} 的財務分析完成。"
        }
        
        # 儲存數據至本地
        with open('market_data.json', 'w', encoding='utf-8') as f:
            json.dump({ticker_symbol: data}, f, ensure_ascii=False, indent=4)
            
        return f"成功為 {ticker_symbol} 獲取數據"
    except Exception as e:
        return f"分析失敗: {str(e)}"
