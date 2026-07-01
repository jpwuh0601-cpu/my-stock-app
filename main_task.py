import sys
import os
import logging

# 加入當前工作目錄到系統路徑，確保能找到同目錄下的 worker.py
sys.path.append(os.getcwd())

import worker

# 設定日誌記錄，確保追蹤執行狀態
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_main_pipeline():
    """
    執行每日主控任務流程
    """
    logging.info(f"當前工作目錄: {os.getcwd()}")
    logging.info("開始執行每日主控任務流程...")
    
    try:
        # 直接呼叫 worker.py 中的分析邏輯
        # 確保 worker.py 中有名為 run_analysis_and_update 的函式
        worker.run_analysis_and_update()
        logging.info("分析任務已順利完成。")
        
    except AttributeError:
        logging.error("錯誤：worker.py 中找不到 run_analysis_and_update 函式，請檢查 worker.py 定義。")
    except ImportError as e:
        logging.error(f"匯入錯誤：無法找到 worker 模組，請確認 worker.py 是否存在且在正確目錄下。細節: {e}")
    except Exception as e:
        logging.error(f"主控流程發生錯誤: {e}")

if __name__ == "__main__":
    run_main_pipeline()
