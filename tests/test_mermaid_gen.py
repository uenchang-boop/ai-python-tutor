"""
Tests for visualizer/mermaid_gen.py — Mermaid 流程圖產生器
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from visualizer.mermaid_gen import (
    generate_call_graph,
    generate_class_diagram,
    generate_sequence_diagram,
)


class TestGenerateCallGraph:
    def test_returns_string(self):
        """generate_call_graph 必須回傳字串"""
        result = generate_call_graph(functions=[], call_graph={})
        assert isinstance(result, str)

    def test_empty_input(self):
        """空白輸入不應拋出例外"""
        result = generate_call_graph(functions=[], call_graph={})
        assert result is not None

    def test_with_functions(self):
        """傳入函數列表應能正常執行"""
        functions = [{"name": "foo", "args": []}, {"name": "bar", "args": ["x"]}]
        call_graph = {"foo": ["bar"]}
        result = generate_call_graph(functions=functions, call_graph=call_graph)
        assert isinstance(result, str)


class TestGenerateClassDiagram:
    def test_returns_string(self):
        """generate_class_diagram 必須回傳字串"""
        result = generate_class_diagram(classes=[])
        assert isinstance(result, str)

    def test_empty_classes(self):
        """空白 classes 不應拋出例外"""
        result = generate_class_diagram(classes=[])
        assert result is not None

    def test_with_class_data(self):
        """傳入 class 資料應能正常執行"""
        classes = [{"name": "MyClass", "methods": ["__init__", "run"], "bases": []}]
        result = generate_class_diagram(classes=classes)
        assert isinstance(result, str)


class TestGenerateSequenceDiagram:
    def test_returns_string(self):
        """generate_sequence_diagram 必須回傳字串"""
        result = generate_sequence_diagram(functions=[], call_graph={})
        assert isinstance(result, str)

    def test_empty_input(self):
        """空白輸入不應拋出例外"""
        result = generate_sequence_diagram(functions=[], call_graph={})
        assert result is not None
