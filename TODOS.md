# TODOS — AI Python Code Tutor

## Visualizer（Round 4）

### P1：Mermaid 流程圖實作
- `visualizer/mermaid_gen.py` 中的 `generate_call_graph()` 實作 Mermaid flowchart 語法
- `generate_class_diagram()` 實作 classDiagram 語法
- `generate_sequence_diagram()` 實作 sequenceDiagram 語法
- 在 `app.py` 中整合 visualizer，於分析結果下方顯示流程圖

### P2：新手引導（Round 4）
- 首次使用的互動式引導流程（Onboarding tour）

## Bug 修復（QA 報告 2026-03-28）

### P1：高優先度
- **原始 HTML 渲染問題**：`call-relation` 區塊顯示原始 HTML 字串（ISSUE-002）
  - 位置：`ui/components.py`，需加入 `unsafe_allow_html=True`
- **語法錯誤提示不可見**：桌機版語法錯誤訊息被藏在空白狀態插圖下方（ISSUE-005）
  - 建議：將錯誤訊息移至結果面板最上方

### P2：中優先度
- **版本號不一致**：標題顯示 v0.2.1，需同步 `APP_VERSION`（ISSUE-001）
- **Streamlit 元件衝突警告**：`code_input` widget 雙重設定問題（ISSUE-003）
- **清除按鈕不重置結果**：點擊清除後右側結果仍顯示（ISSUE-004）

### P3：低優先度
- **無障礙設計**：Radio button ARIA 元素無法直接互動（ISSUE-006）

## Completed

- [x] Round 3：Class 解析器（ClassDef）— v0.3.0.0 (2026-03-15)
- [x] Round 3：Import 解析器（import encyclopedia）— v0.3.0.0 (2026-03-15)
- [x] Round 3：Gemini API 雙模式支援 — v0.3.0.0 (2026-03-15)
- [x] Round 2：Gemini AI 解釋引擎 + 快取 — v0.2.1.0 (2026-02-10)
- [x] visualizer 骨架建立（Round 4 準備）— v0.3.1.0 (2026-03-28)
- [x] pytest 測試框架設定 — v0.3.1.0 (2026-03-28)
