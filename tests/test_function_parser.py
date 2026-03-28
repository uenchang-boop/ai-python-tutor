"""
Tests for parsers/function_parser.py — 函數解析器
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.function_parser import parse_functions


class TestParseFunctions:
    def test_empty_code(self):
        """空字串不應拋出例外，回傳空函數列表"""
        result = parse_functions("")
        assert isinstance(result, dict)
        assert "functions" in result
        assert len(result["functions"]) == 0

    def test_single_function(self):
        """單一函數應被正確解析"""
        code = "def hello():\n    pass\n"
        result = parse_functions(code)
        assert len(result["functions"]) == 1
        assert result["functions"][0]["name"] == "hello"

    def test_function_with_args(self):
        """帶參數的函數應解析出正確參數"""
        code = "def greet(name, greeting='Hi'):\n    return f'{greeting} {name}'\n"
        result = parse_functions(code)
        assert len(result["functions"]) == 1
        assert "name" in result["functions"][0]["params"]

    def test_multiple_functions(self):
        """多個函數應全部被解析"""
        code = "def foo():\n    pass\n\ndef bar():\n    pass\n"
        result = parse_functions(code)
        assert len(result["functions"]) == 2

    def test_invalid_syntax_no_crash(self):
        """語法錯誤的程式碼應回傳 errors，不拋出例外"""
        code = "def broken(:\n    pass\n"
        result = parse_functions(code)
        assert isinstance(result, dict)
        # 應該有 errors 或空 functions
        assert "errors" in result or len(result.get("functions", [])) == 0

    def test_docstring_captured(self):
        """有 docstring 的函數應被捕捉到"""
        code = 'def foo():\n    """這是說明\"\"\"\n    pass\n'
        result = parse_functions(code)
        assert len(result["functions"]) == 1
        assert result["functions"][0]["docstring"] is not None

    def test_top_level_code_detected(self):
        """頂層程式碼應被偵測"""
        code = "x = 1\n\ndef foo():\n    pass\n\nif __name__ == '__main__':\n    foo()\n"
        result = parse_functions(code)
        assert "top_level_code" in result
