def load_market_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                # 若讀取內容為 None，回傳空字典作為預設值
                return data if data is not None else {}
        except (json.JSONDecodeError, Exception) as e:
            st.warning("數據檔案格式錯誤，正在嘗試修復...")
            return {}
    return {}
```

### 2. 在渲染前檢查資料是否存在
在 `app.py` 渲染「籌碼面分析」或「AI 預測」區塊前，請務必先確認該鍵值是否存在，避免直接存取：

```python
# 錯誤的存取方式 (可能導致 NoneType Error)
# st.write(market_data['institutional_investors'])

# 建議的正確存取方式 (使用 .get() 並提供預設值)
investors = market_data.get('institutional_investors', [])
if investors:
    st.write(f"外資買賣超: {investors[0].get('買賣超', 'N/A')}")
else:
    st.write("目前無外資籌碼數據。")
```

### 3. 檢查 JSON 檔案格式
因為您的截圖顯示 `market_data.json` 可能在 GitHub Action 推送後格式跑掉，請您執行以下動作確認檔案內容：
1. 前往您的 GitHub 倉庫。
2. 點開 `market_data.json`。
3. 確保它看起來像這樣（正確的 JSON 格式）：
   ```json
   {
       "ticker": "2330",
       "price": 1000.0,
       "institutional_investors": [{"機構": "外資", "買賣超": 500}]
   }
