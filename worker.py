name: Daily Stock Analysis
on:
schedule:
- cron: '30 0 * * *'
workflow_dispatch:
jobs:
run-script:
runs-on: ubuntu-latest
steps:
- uses: actions/checkout@v3
- name: Set up Python
uses: actions/setup-python@v4
with:
python-version: '3.9'
- name: Install dependencies
run: |
pip install twstock pandas openai requests
- name: Run worker script
env:
OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
LINE_CHANNEL_ACCESS_TOKEN: ${{ secrets.LINE_CHANNEL_ACCESS_TOKEN }}
GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
GOOGLE_CSE_ID: ${{ secrets.GOOGLE_CSE_ID }}
run: |
python worker.py
