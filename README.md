# 🐍 AI Python Code Tutor — Round 2

> **貼上程式碼 → 秒懂每個函數在做什麼**
> 由 Google Gemini AI 驅動，支援離線模式

---

## 🚀 快速啟動

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 啟動應用
streamlit run app.py
```

瀏覽器會自動打開 `http://localhost:8501`

---

## 🔑 設定 Gemini API Key

1. 前往 [Google AI Studio](https://aistudio.google.com/app/apikey) 免費取得 API Key
2. 在 Streamlit 左側欄貼上 Key
3. 選擇模型（預設 `gemini-2.0-flash`）

> **不想申請 Key？** 選「離線模式」，使用內建關鍵字模板解釋函數。

---

## 🔁 切換回 Claude API（彈性設計）

本專案的 AI 層設計為**可快速切換**。

### 改回 Claude API 步驟

**1. 修改 `requirements.txt`**
```
anthropic>=0.30.0   # 取消這行的 #
# google-generativeai>=0.8.0   # 可以保留或移除
```

**2. 修改 `ai/explainer.py`** — 只需替換 `init_ai()` 和 `_call_gemini()` 兩個函式：

```python
# init_ai() 改為：
def init_ai(api_key: str, model: str = "claude-sonnet-4-20250514") -> bool:
    global _api_client, _current_model, _api_ready
    if not api_key:
        _api_ready = False
        return False
    try:
        import anthropic
        _api_client  = anthropic.Anthropic(api_key=api_key.strip())
        _current_model = model
        _api_ready   = True
        return True
    except Exception:
        _api_ready = False
        return False

# _call_gemini() 改名為 _call_claude()：
def _call_claude(func_info: dict, code: str) -> dict:
    prompt   = FUNCTION_EXPLAIN_PROMPT.format(code_snippet=code)
    response = _api_client.messages.create(
        model=_current_model,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    raw_text = response.content[0].text.strip()
    # ... 後續 JSON 解析邏輯不變
```

**3. 修改 `config.py`** — 加回 Claude 設定：
```python
CLAUDE_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODELS = ["claude-sonnet-4-20250514", "claude-haiku-4-5-20251001"]
```

**4. 修改 `ui/sidebar.py`** — API Key placeholder 改為 `sk-ant-...`

---

## 📁 專案結構

```
ai-python-tutor/
├── app.py                    # Streamlit 主程式
├── config.py                 # 全域設定（API key、快取路徑）
├── requirements.txt
│
├── parsers/                  # 程式碼解析（ast 模組）
│   ├── function_parser.py    # FunctionDef 解析
│   ├── call_graph.py         # 函數呼叫關係分析
│   ├── class_parser.py       # ClassDef 解析（第 3 輪完整實作）
│   └── import_parser.py      # Import 解析（第 3 輪完整實作）
│
├── ai/                       # AI 解釋模組
│   ├── explainer.py          # 主解釋函式（Gemini + fallback）
│   ├── prompts.py            # Prompt 模板
│   └── cache.py              # SHA256 快取（JSON 檔案）
│
├── ui/                       # UI 元件
│   ├── theme.py              # Claude 風格 CSS
│   ├── components.py         # 函數卡片、摘要列等元件
│   └── sidebar.py            # API Key 設定側邊欄
│
└── cache/                    # 快取資料夾（自動產生）
```

---

## ✨ 第 2 輪新功能

| 功能 | 說明 |
|------|------|
| 🤖 Gemini AI 解釋 | 每個函數由 AI 產生智慧解說 |
| ⚡ 快取機制 | SHA256 hash + JSON 檔案，7 天 TTL |
| 📊 命中率統計 | 側邊欄顯示節省的 API 費用 |
| 📌 參數解釋表 | AI 解釋每個參數的用途 |
| 🟢🟡🔴 複雜度標示 | simple / medium / complex |
| 📖 離線 fallback | 無 Key 時自動使用關鍵字模板 |

---

## 🗺️ 開發藍圖

| 輪次 | 狀態 | 功能 |
|------|------|------|
| Round 1 | ✅ 完成 | 核心解析 + UI 骨架 |
| Round 2 | ✅ 完成 | Gemini AI + 快取 |
| Round 3 | 🔜 | Class 解析 + Import 百科 |
| Round 4 | 🔜 | Mermaid 流程圖 + 新手引導 |
