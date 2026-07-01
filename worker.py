import worker
import logging

logging.basicConfig(level=logging.INFO)

def run_main_pipeline():
    logging.info("開始執行主流程")
    # 直接呼叫函式
    worker.run_analysis_and_update()
    logging.info("執行完畢")

if __name__ == "__main__":
    run_main_pipeline()
```

#### 步驟 3：強制清除 GitHub 快取並重新推送
在您的電腦終端機，執行以下指令，這是為了確保 Git 強制抓取最新檔案並清理任何可能導致錯誤的緩存：

```bash
# 1. 確保加入這些檔案
git add worker.py main_task.py

# 2. 強制 Commit 變更
git commit -m "fix: 徹底同步函式名稱與結構"

# 3. 強制推送到 GitHub
git push origin main
