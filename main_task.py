import argparse
import sys
import os
import importlib.util

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', type=str, required=True, help="股票代號")
    args = parser.parse_args()

    # 動態載入 worker 模組
    worker_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "worker.py")
    spec = importlib.util.spec_from_file_location("worker", worker_path)
    worker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(worker)

    # 執行分析
    result = worker.get_ai_analysis(args.ticker)
    print(result)

if __name__ == "__main__":
    run()
