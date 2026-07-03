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

    # 升級後的 Prompt：讓 AI 讀取更多欄位並給出結構化建議
    prompt = f"""
    請針對以下台積電 (2330.TW) 的最新財報數據，給出專業的市場分析意見：
    - 當前股價: {data.get('price')}
    - 每股淨值: {data.get('bvps')}
    - 法人籌碼動向: {data.get('institutional_investors')}
    
    請以專業投資顧問的角度，簡短分析目前趨勢（建議買入/賣出/觀望），並說明理由，不超過 100 字。
    """

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"AI 分析失敗: {e}")
        return "AI 分析模組暫時無法使用。"

def send_line_notify(message):
    """透過 LINE Notify 發送通知"""
    token = os.getenv("LINE_NOTIFY_TOKEN")
    if not token:
        return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    requests.post(url, headers=headers, data={"message": message})

def run_analysis_and_update():
    """執行市場數據抓取、AI 分析並更新 JSON"""
    ticker_symbol = "2330.TW"
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        price = ticker.fast_info.last_price
        
        # 準備資料結構，納入更多指標
        raw_data = {
            "price": price,
            "bvps": info.get("bookValue", 0),
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
