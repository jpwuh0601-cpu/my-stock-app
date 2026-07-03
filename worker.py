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
    
    # 嚴格驗證：檢查 Key 是否存在與長度
    if not api_key:
        logging.error("【嚴重錯誤】系統讀取不到 OPENROUTER_API_KEY，請確認 GitHub Secrets 設定。")
        return "AI 分析模組未設定 API Key。"
    
    # 偵錯用：確認 Key 的長度是否正確 (sk-or-v1 開頭的 Key 長度通常固定)
    logging.info(f"API Key 已載入，長度為: {len(api_key)}")

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key.strip(), # 強制去除前後空格與換行
        )

        model_name = "google/gemini-2.0-flash-exp" 

        prompt = f"""
        請針對以下台積電 (2330.TW) 的數據，給出專業的投資分析建議（不超過100字）：
        - 股價: {data.get('price')}
        - 籌碼: {data.get('institutional_investors')}
        """

        completion = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        # 特別處理 401 錯誤，告知您可能是 Key 無效或授權不足
        if "401" in str(e):
             logging.error("【認證失敗】401 Unauthorized。請檢查 OPENROUTER_API_KEY 是否有效，或者在 OpenRouter 網站上檢查該 Key 是否有權限呼叫此模型。")
        logging.error(f"【詳細除錯資訊】錯誤類型: {type(e).__name__}, 錯誤詳情: {str(e)}")
        return f"AI 分析發生錯誤: {type(e).__name__}"

def send_line_notify(message):
    token = os.getenv("LINE_NOTIFY_TOKEN")
    if not token:
        logging.warning("LINE Notify Token 未設定。")
        return
        
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token.strip()}"}
    try:
        requests.post(url, headers=headers, data={"message": message}).raise_for_status()
    except Exception as e:
        logging.error(f"LINE 通知發送失敗: {e}")

def run_analysis_and_update():
    ticker_symbol = "2330.TW"
    try:
        ticker = yf.Ticker(ticker_symbol)
        price = ticker.fast_info.last_price
        
        raw_data = {
            "price": price,
            "institutional_investors": [{"機構": "外資", "買賣超": 500}],
        }
        
        raw_data["ai_prediction"] = get_ai_analysis(raw_data)
        
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=4)
        
        msg = f"\n📈 台積電分析報告\n股價: {price:.2f}\nAI觀點: {raw_data['ai_prediction']}"
        send_line_notify(msg)
        
        logging.info("數據與 AI 分析更新完成")
            
    except Exception as e:
        logging.error(f"執行錯誤: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
