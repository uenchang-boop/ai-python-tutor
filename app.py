"""
AI Python Code Tutor — 主程式入口
第 3 輪 v3：新增 Class 解析 + Import 百科
"""
import html as _html_mod
import streamlit as st

from config import APP_TITLE, APP_ICON, SAMPLE_CODE
from parsers.function_parser import parse_functions
from parsers.class_parser    import parse_classes
from parsers.import_parser   import parse_imports_detail
from parsers.call_graph      import build_call_graph
from ai.explainer import (
    generate_explanation,
    generate_class_explanation,
    generate_import_explanation,
    init_ai, get_cache,
    is_api_ready, get_session_cost, reset_session_cost,
)
from ui.theme import inject_theme
from ui.components import (
    render_header, render_welcome, render_summary_bar,
    render_function_card, render_top_level_code, render_import_tags,
    render_class_card, render_import_encyclopedia,
)
from ui.sidebar import render_sidebar


def _esc(s: str) -> str:
    return _html_mod.escape(s)



# ── 第 3 輪：擴充摘要列（含類別數）─────────────────────
def render_summary_bar_v3(result: dict):
    """擴充版摘要列，含函數、類別、套件、頂層程式碼數量。"""
    func_count   = len([f for f in result.get("functions", []) if not f.get("parent_class")])
    class_count  = len(result.get("classes", []))
    import_count = len(result.get("imports", []))
    toplevel     = result.get("top_level_code", [])

    tags = []
    if func_count:
        tags.append(f'<span class="summary-tag tag-func">🔧 {func_count} 個函數</span>')
    if class_count:
        tags.append(
            f'<span class="summary-tag" style="background:#EDE9FE;color:#5B21B6;">'
            f'🏛️ {class_count} 個類別</span>'
        )
    if import_count:
        tags.append(f'<span class="summary-tag tag-import">📦 {import_count} 個套件</span>')
    if toplevel:
        tags.append(f'<span class="summary-tag tag-top">📄 {len(toplevel)} 段頂層程式碼</span>')

    if tags:
        st.markdown(
            f'<div class="summary-bar">{"".join(tags)}</div>',
            unsafe_allow_html=True,
        )

# ── 頁面設定 ─────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme()

# ── Session State 初始化 ──────────────────────────────
for key, default in [
    ("analysis_result",    None),
    ("classes_result",     []),
    ("import_details",     []),
    ("call_graph",         {}),
    ("code_input",         ""),
    ("last_analyzed_code", ""),
    ("provider_choice",    "🤖 Claude API"),
    ("last_cost",          None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── 側邊欄 ───────────────────────────────────────────
sidebar_cfg = render_sidebar()
api_key     = sidebar_cfg["api_key"]
model       = sidebar_cfg["model"]
provider    = sidebar_cfg["provider"]
mode        = sidebar_cfg["mode"]

if mode not in ("offline",) and api_key:
    init_ai(api_key, model, provider)

# ── 標題 ─────────────────────────────────────────────
render_header()

# ── 主佈局 ───────────────────────────────────────────
col_input, col_spacer, col_output = st.columns([5, 0.3, 6])

# ═══════════════════════════════════════════════════
#  左欄：程式碼輸入
# ═══════════════════════════════════════════════════
with col_input:
    st.markdown(
        '<div style="font-size:15px;font-weight:600;color:#1A1A1A;margin-bottom:10px;">'
        '📝 貼上你的 Python 程式碼</div>',
        unsafe_allow_html=True,
    )

    if st.button("📋 載入範例程式碼", use_container_width=True, type="secondary"):
        st.session_state["code_input"] = SAMPLE_CODE
        st.rerun()

    def clear_code_input():
        st.session_state["code_input"] = ""

    code = st.text_area(
        label="code_area",
        value=st.session_state.get("code_input", ""),
        height=440,
        placeholder="# 在這裡貼上 Python 程式碼...\n\ndef hello():\n    pass",
        label_visibility="collapsed",
        key="code_input",
    )

    col_analyze, col_clear = st.columns([3, 1])
    with col_analyze:
        analyze_btn = st.button(
            "🔍 開始分析",
            use_container_width=True,
            type="primary",
            disabled=not code.strip(),
        )
    with col_clear:
        if st.button("🗑️ 清除", use_container_width=True, type="secondary", on_click=clear_code_input):
            st.rerun()

    if code.strip():
        lines = code.count("\n") + 1
        chars = len(code)
        st.caption(f"📏 共 {lines:,} 行 · {chars:,} 字元")

    st.markdown("---")

    if is_api_ready():
        prov_label = "Claude" if provider == "claude" else "Gemini"
        st.markdown(
            f'<div style="font-size:12px;color:#059669;line-height:1.7;">'
            f'🤖 {prov_label} AI 已就緒，將為每個函數產生智慧解釋<br>'
            f'⚡ 快取命中時直接讀取，節省 API 費用'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="font-size:12px;color:#9B9B9B;line-height:1.7;">'
            '📖 目前為離線模式（關鍵字模板）<br>'
            '💡 在左側欄輸入 API Key 啟用 AI 解釋'
            '</div>',
            unsafe_allow_html=True,
        )

# ═══════════════════════════════════════════════════
#  右欄：分析結果
# ═══════════════════════════════════════════════════
with col_output:

    # ── 觸發分析 ────────────────────────────────────
    if analyze_btn and code.strip():
        reset_session_cost()
        with st.spinner("🔍 正在解析程式碼..."):
            result  = parse_functions(code)
            classes = parse_classes(code)
            imports = parse_imports_detail(code)

        if result["errors"]:
            for err in result["errors"]:
                st.error(f"⚠️ {err}")
            st.session_state.analysis_result = None
            st.session_state.classes_result  = []
            st.session_state.import_details  = []
            st.session_state.call_graph       = {}
            st.session_state.last_analyzed_code = ""
        else:
            cg = build_call_graph(result["functions"])
            st.session_state.analysis_result    = result
            st.session_state.classes_result     = classes
            st.session_state.import_details     = imports
            st.session_state.call_graph         = cg
            st.session_state.last_analyzed_code = code

    # ── 顯示結果 ─────────────────────────────────────
    result  = st.session_state.analysis_result
    classes = st.session_state.classes_result
    imports = st.session_state.import_details
    cg      = st.session_state.call_graph

    if result is not None:
        funcs     = result.get("functions", [])
        top_level = result.get("top_level_code", [])

        # 摘要列（新增類別數量）
        _render_result = dict(result)
        _render_result["classes"]   = classes
        render_summary_bar_v3(_render_result)

        # ── Import 百科（優先顯示）──────────────────
        if imports:
            ai_fn = generate_import_explanation if is_api_ready() else None
            render_import_encyclopedia(imports, ai_explain_fn=ai_fn)
            st.markdown("---")

        # ── 獨立函數區（無 parent_class）──────────
        standalone = [f for f in funcs if not f.get("parent_class")]

        if standalone:
            st.markdown(
                '<div style="font-size:13px;font-weight:700;color:#6B6B6B;'
                'letter-spacing:0.5px;margin-bottom:10px;margin-top:4px;">'
                '🔧 函數列表</div>',
                unsafe_allow_html=True,
            )
            if is_api_ready():
                prog_bar = st.progress(0, text="🤖 正在向 AI 詢問解釋...")

            for i, func in enumerate(standalone):
                explanation = generate_explanation(func)
                relations   = cg.get(func["name"], {})
                render_function_card(func, explanation, relations)
                if is_api_ready():
                    prog_bar.progress(
                        (i + 1) / len(standalone),
                        text=f"✅ {i+1}/{len(standalone)} 個函數解釋完成",
                    )

            if is_api_ready():
                prog_bar.empty()
            st.session_state["last_cost"] = get_session_cost()

        # ── 類別區（階層式顯示）─────────────────────
        if classes:
            st.markdown(
                '<div style="font-size:13px;font-weight:700;color:#6B6B6B;'
                'letter-spacing:0.5px;margin-bottom:10px;margin-top:20px;">'
                '🏛️ 類別列表</div>',
                unsafe_allow_html=True,
            )

            if is_api_ready():
                cls_prog = st.progress(0, text="🤖 正在解釋類別...")

            for ci, class_info in enumerate(classes):
                # 類別本體解釋
                class_expl = generate_class_explanation(class_info)
                # 各方法解釋
                method_expls = {}
                methods = class_info.get("methods", [])
                for method in methods:
                    method_expls[method["name"]] = generate_explanation(method)
                render_class_card(class_info, class_expl, method_expls, cg)

                if is_api_ready():
                    cls_prog.progress(
                        (ci + 1) / len(classes),
                        text=f"✅ {ci+1}/{len(classes)} 個類別解釋完成",
                    )

            if is_api_ready():
                cls_prog.empty()
            st.session_state["last_cost"] = get_session_cost()

        if not standalone and not classes and not top_level:
            st.info("ℹ️ 沒有偵測到函數或類別定義，但程式碼解析成功。")

        if top_level:
            render_top_level_code(top_level)

        # ── 底部統計列 ───────────────────────────────
        st.markdown("---")
        cache = get_cache()
        stats = cache.stats()

        col_stat, col_cost = st.columns([1, 1])

        with col_stat:
            hit_pct = int(stats["hit_rate"] * 100)
            st.markdown(
                f'<div style="font-size:12px;color:#6B6B6B;">'
                f'⚡ 快取命中 {stats["hits"]} &nbsp;/&nbsp; '
                f'🤖 API 呼叫 {stats["misses"]} &nbsp;·&nbsp; 命中率 {hit_pct}%'
                f'</div>',
                unsafe_allow_html=True,
            )

        with col_cost:
            cost = st.session_state.get("last_cost") or get_session_cost()
            if cost and cost.get("api_calls", 0) > 0:
                usd     = cost["total_usd"]
                in_tok  = cost["input_tokens"]
                out_tok = cost["output_tokens"]
                calls   = cost["api_calls"]
                twd     = usd * 32
                st.markdown(
                    f'<div style="font-size:12px;color:#059669;text-align:right;'
                    f'background:#F0FDF4;padding:8px 12px;border-radius:8px;">'
                    f'💰 本次查詢消耗費用<br>'
                    f'<span style="font-size:16px;font-weight:700;color:#065F46;">'
                    f'${usd:.5f} USD</span>'
                    f'<span style="color:#9B9B9B;font-size:12px;"> ≈ NT${twd:.3f}</span><br>'
                    f'<span style="color:#6B6B6B;font-size:11px;">'
                    f'📥 輸入 {in_tok:,} / 📤 輸出 {out_tok:,} tokens'
                    f'&nbsp;·&nbsp; 共 {calls} 次呼叫'
                    f'</span></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div style="font-size:12px;color:#9B9B9B;text-align:right;">'
                    '💰 本次費用：$0.00000（快取命中 / 離線模式）</div>',
                    unsafe_allow_html=True,
                )

    else:
        render_welcome()
