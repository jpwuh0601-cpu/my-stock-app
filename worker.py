import json
import logging
import yfinance as yf
import os
import requests
from openai import OpenAI

# 設定日誌
logging.basicConfig(level=logging.INFO)

def get_ai_analysis(data):
    """呼叫 OpenRouter/OpenAI 生成分析"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "AI 分析模組未設定 API Key。"

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    prompt = f"""
    請針對以下台積電 (2330.TW) 的數據進行簡短的市場分析（兩句話內）：
    股價: {data.get('price')}
    本益比: {data.get('pe_ratio')}
    每股盈餘預測: {data.get('eps_forecast')}
    法人籌碼: {data.get('institutional_investors')}
    """

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"AI 分析失敗: {e}")
        return "目前無法生成 AI 分析。"

def send_line_notify(message):
    token = os.getenv("LINE_NOTIFY_TOKEN")
    if not token:
        return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    requests.post(url, headers=headers, data={"message": message})

def run_analysis_and_update():
    ticker_symbol = "2330.TW"
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        price = ticker.fast_info.last_price
        
        # 準備資料結構
        raw_data = {
            "price": price,
            "pe_ratio": info.get("trailingPE", 0),
            "eps_forecast": info.get("trailingEps", 0),
            "institutional_investors": [{"機構": "外資", "買賣超": 500}, {"機構": "投信", "買賣超": 200}],
        }
        
        # 執行 AI 分析
        raw_data["ai_prediction"] = get_ai_analysis(raw_data)
        
        # 儲存到 JSON
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=4)
        
        # 發送 LINE 通知
        msg = f"\n📈 台積電分析報告\n股價: {price:.2f}\nAI觀點: {raw_data['ai_prediction']}"
        send_line_notify(msg)
        
        logging.info("數據與 AI 分析更新完成")
            
    except Exception as e:
        logging.error(f"執行錯誤: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
