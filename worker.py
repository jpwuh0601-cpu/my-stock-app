```python id="h7qvso"
import json
import logging
import yfinance as yf
import os
import requests
from openai import OpenAI
from datetime import datetime

# =========================
# 日誌設定
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================
# AI 分析
# =========================
def get_ai_analysis(data):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        logging.error("找不到 OPENROUTER_API_KEY")
        return "AI 模組未設定 API Key"

    try:

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

        prompt = f"""
你是一位專業台股分析師。

請針對以下台積電（2330.TW）數據，
給出 80 字內專業分析：

目前股價：{data.get('price')}
每股淨值：{data.get('bvps')}
本益比：{data.get('pe')}
市場風險：{data.get('risk_level')}
法人動向：{data.get('institutional_investors')}

請直接分析：
1. 趨勢
2. 風險
3. 建議（買進/觀望/減碼）
"""

        completion = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=200
        )

        result = completion.choices[0].message.content

        return result.strip()

    except Exception as e:

        logging.error(f"AI 分析失敗: {type(e).__name__}: {e}")

        return "AI 分析暫時失敗"

# =========================
# LINE 通知
# =========================
def send_line_notify(message):

    token = os.getenv("LINE_NOTIFY_TOKEN")

    if not token:
        logging.warning("LINE_NOTIFY_TOKEN 未設定")
        return

    url = "https://notify-api.line.me/api/notify"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = {
        "message": message
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            data=data,
            timeout=15
        )

        response.raise_for_status()

        logging.info("LINE 通知成功")

    except Exception as e:

        logging.error(f"LINE 通知失敗: {e}")

# =========================
# 風險分析
# =========================
def calculate_risk(change_percent):

    if change_percent <= -3:
        return "高"

    elif change_percent <= -1:
        return "中"

    else:
        return "低"

# =========================
# 主分析流程
# =========================
def run_analysis_and_update():

    ticker_symbol = "2330.TW"

    try:

        logging.info("開始抓取股票資料")

        ticker = yf.Ticker(ticker_symbol)

        info = ticker.info

        hist = ticker.history(period="2d")

        # =========================
        # 安全取值
        # =========================
        current_price = float(
            info.get("currentPrice", 0)
        )

        previous_close = float(
            info.get("previousClose", current_price)
        )

        change = current_price - previous_close

        change_percent = (
            (change / previous_close) * 100
            if previous_close != 0 else 0
        )

        volume = int(
            info.get("volume", 0)
        )

        pe_ratio = info.get("trailingPE", 0)

        bvps = info.get("bookValue", 0)

        # =========================
        # 風險等級
        # =========================
        risk_level = calculate_risk(change_percent)

        # =========================
        # 法人模擬資料
        # =========================
        institutional_data = [
            {
                "機構": "外資",
                "買賣超": "+5200"
            },
            {
                "機構": "投信",
                "買賣超": "+800"
            },
            {
                "機構": "自營商",
                "買賣超": "-200"
            }
        ]

        # =========================
        # 建立資料
        # =========================
        raw_data = {
            "stock_id": ticker_symbol,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "price": round(current_price, 2),

            "change": round(change, 2),

            "change_percent": round(change_percent, 2),

            "volume": volume,

            "pe": pe_ratio,

            "bvps": bvps,

            "risk_level": risk_level,

            "institutional_investors": institutional_data
        }

        # =========================
        # AI 分析
        # =========================
        logging.info("開始 AI 分析")

        raw_data["ai_prediction"] = get_ai_analysis(raw_data)

        # =========================
        # 儲存 JSON
        # =========================
        with open(
            "market_data.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                raw_data,
                f,
                ensure_ascii=False,
                indent=4
            )

        logging.info("market_data.json 更新完成")

        # =========================
        # LINE 推播
        # =========================
        message = f"""
📈 台積電 AI 分析

股價：{current_price:.2f}
漲跌：{change:+.2f} ({change_percent:+.2f}%)

風險等級：{risk_level}

AI 分析：
{raw_data['ai_prediction']}
"""

        send_line_notify(message)

        logging.info("全部流程完成")

    except Exception as e:

        logging.error(f"主程式錯誤: {type(e).__name__}: {e}")

# =========================
# 執行
# =========================
if __name__ == "__main__":

    run_analysis_and_update()
```
