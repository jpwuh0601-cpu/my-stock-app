import sys
import os

# 強制將當前目錄加入 Python 搜尋路徑，確保可以找到 worker.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import worker
import logging

logging.basicConfig(level=logging.INFO)

def run_main_pipeline():
    logging.info("開始執行主流程")
    try:
        # 確保呼叫的函式名稱與 worker.py 裡的一模一樣
        worker.run_analysis_and_update()
        logging.info("執行完畢")
    except AttributeError as e:
        logging.error(f"找不到函式: {e}")
    except Exception as e:
        logging.error(f"發生未知錯誤: {e}")

if __name__ == "__main__":
    run_main_pipeline()
