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
    # 這裡會自動讀取 GitHub Secrets 中設定的 OPENROUTER_API_KEY
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        logging.error("找不到 API Key，請確認 GitHub Secrets 設定。")
        return "AI 分析模組未設定 API Key。"

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        prompt = f"""
        請針對以下台積電 (2330.TW) 的最新財報數據，給出專業的市場分析意見：
        - 當前股價: {data.get('price')}
        - 每股淨值: {data.get('bvps')}
        - 法人籌碼動向: {data.get('institutional_investors')}
        
        請以專業投資顧問的角度，簡短分析目前趨勢（建議買入/賣出/觀望），並說明理由，不超過 100 字。
        """

        completion = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"AI 分析詳細錯誤: {type(e).__name__}: {e}")
        return f"AI 分析發生錯誤: {type(e).__name__}"

def send_line_notify(message):
    """透過 LINE Notify 發送通知"""
    # 這裡建議使用 LINE_NOTIFY_TOKEN (與程式碼中的變數名一致)
    token = os.getenv("LINE_NOTIFY_TOKEN")
    if not token:
        logging.warning("LINE Notify Token 未設定。")
        return
        
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(url, headers=headers, data={"message": message})
        response.raise_for_status()
    except Exception as e:
        logging.error(f"LINE 通知發送失敗: {e}")

def run_analysis_and_update():
    """執行市場數據抓取、AI 分析並更新 JSON"""
    ticker_symbol = "2330.TW"
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        price = ticker.fast_info.last_price
        
        # 準備資料結構
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
