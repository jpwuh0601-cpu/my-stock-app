import sys
import os

# 確保當前目錄在系統路徑中，讓 Python 能順利找到 worker.py
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    import worker
except ImportError as e:
    print(f"錯誤：無法匯入 worker 模組，請確保 worker.py 位於 {current_dir} 目錄下。")
    raise e

def run():
    # 執行 worker 中的分析函數
    worker.run_analysis_and_update()

if __name__ == "__main__":
    run()
