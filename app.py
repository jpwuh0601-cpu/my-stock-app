name: Daily Stock Analysis
on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      # 修正：使用 --upgrade 確保套件版本為最新，並處理相依性衝突
      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install --upgrade yfinance requests pandas
          
      - run: python main_task.py
      
      - name: 推送數據
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add market_data.json
          git commit -m "chore: update market_data.json" || exit 0
          git push origin main
