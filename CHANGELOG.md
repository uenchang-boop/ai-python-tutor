# Changelog

All notable changes to AI Python Code Tutor will be documented in this file.

## [0.3.1.0] - 2026-03-28

### Added
- 新增 `visualizer/` 套件（Round 4 Mermaid.js 視覺化骨架）
- `generate_call_graph()` stub — 函數呼叫關係流程圖（待 Round 4 實作）
- `generate_class_diagram()` stub — Class 繼承關係圖（待 Round 4 實作）
- `generate_sequence_diagram()` stub — 函數執行順序圖（待 Round 4 實作）
- pytest 測試框架：15 個單元測試，覆蓋率 73%

### Changed
- `visualizer/mermaid_gen.py` 加上完整型別標註與 docstrings（pre-landing review auto-fix）

## [0.3.0.0] - 2026-03-15

### Added
- Round 3: Class parser (ClassDef analysis)
- Round 3: Import parser (import encyclopedia)
- Gemini API support alongside Claude API
- Dual-mode provider switching (Claude / Gemini / Offline)
- Cost estimator per session

### Changed
- Version bump to 0.3.x series

## [0.2.1.0] - 2026-02-10

### Added
- Round 2: Gemini AI explanation engine
- SHA256 cache with 7-day TTL
- Cache hit-rate statistics in sidebar
- Complexity badges (simple / medium / complex)
- Offline fallback mode with keyword templates
