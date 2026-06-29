import json
import os
# ... (您的 OpenAI / OpenRouter 呼叫邏輯)

def validate_data(data):
    """自動回測數據準確性"""
    required_keys = ['price', 'bvps', 'financials', 'institutional_investors']
    for key in required_keys:
        if key not in data:
            raise ValueError(f"數據驗證失敗：缺少 {key}")
    print("數據回測成功：所有關鍵欄位皆正確。")

# 假設這是您組合好的最終數據
# final_data = { ... }

# 在寫入前執行驗證
# validate_data(final_data)

# 寫入檔案
# with open("market_data.json", "w", encoding="utf-8") as f:
#     json.dump(final_data, f, ensure_ascii=False, indent=4)
