import json
import os
import requests
import logging

logging.basicConfig(level=logging.INFO)

def run_analysis_and_update():
    # 這裡放您的數據抓取與 AI 分析邏輯
    data = {
        "price": 1050.0,
        "ai_prediction": "分析結果正常"
    }
    
    # 修改寫入方式：使用暫存檔
    temp_file = "market_data.json.tmp"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        # 確保寫入成功後才更換檔案名稱，這能防止 JSONDecodeError
        os.replace(temp_file, "market_data.json")
        logging.info("market_data.json 更新成功")
    except Exception as e:
        logging.error(f"寫入檔案時發生錯誤: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
