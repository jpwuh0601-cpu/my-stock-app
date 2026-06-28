name: AI 自動化健檢與日記任務

on:
  schedule:
    - cron: '30 0 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          persist-credentials: true

      - name: 設定 Python 環境
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: 安裝套件
        run: |
          pip install pandas requests yfinance openai beautifulsoup4

      - name: 執行分析並儲存
        env:
          LINE_NOTIFY_TOKEN: ${{ secrets.LINE_NOTIFY_TOKEN }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python worker.py

      - name: 推送更新至 GitHub
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add journal.json
          git commit -m "chore: auto-update daily journal" || echo "No changes to commit"
          git push
