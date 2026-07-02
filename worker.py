import sys
import os
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)

# 將當前腳本所在的目錄加入系統路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def run_main_pipeline():
    logging.info(f"當前工作目錄: {os.getcwd()}")
    logging.info(f"腳本目錄: {current_dir}")
    
    # 檢查 worker.py 是否存在
    if not os.path.exists(os.path.join(current_dir, "worker.py")):
        logging.error("致命錯誤：在目錄中找不到 worker.py")
        return

    try:
        import worker
        logging.info("成功導入 worker 模組")
        worker.run_analysis_and_update()
        logging.info("分析任務執行完畢")
    except ImportError as e:
        logging.error(f"導入模組失敗: {e}")
    except Exception as e:
        logging.error(f"發生未知錯誤: {e}")

if __name__ == "__main__":
    run_main_pipeline()
