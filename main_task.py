import sys
import os
import traceback

# 確保當前目錄在系統路徑中，讓 Python 能順利找到 worker.py
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    import worker
except ImportError as e:
    print(f"致命錯誤：無法匯入 worker 模組。請確認 worker.py 是否存在於 {current_dir}")
    print(f"錯誤詳情: {e}")
    sys.exit(1)

def run():
    """
    執行 worker 中的分析函數，並加入錯誤捕捉機制
    確保主流程不會因為單一錯誤直接崩潰
    """
    try:
        print("正在啟動分析程序...")
        worker.run_analysis_and_update()
        print("分析程序已順利完成。")
    except Exception as e:
        print("執行分析程序時發生錯誤:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run()
