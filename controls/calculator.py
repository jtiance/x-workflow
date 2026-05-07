# -*- coding: utf-8 -*-
"""
计算器控件模块
对文本中的数学表达式进行安全求值
"""

import ast
import operator
import math

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QSizePolicy
from qfluentwidgets import LineEdit, BodyLabel, ComboBox

from controls.base_control import BaseControl


# 支持的运算符
_SUPPORTED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# 支持的 math 函数
_SUPPORTED_FUNCTIONS = {
    'sqrt': math.sqrt,
    'abs': abs,
    'round': round,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,
    'log10': math.log10,
    'log2': math.log2,
    'exp': math.exp,
    'ceil': math.ceil,
    'floor': math.floor,
    'radians': math.radians,
    'degrees': math.degrees,
    'pow': pow,
    'min': min,
    'max': max,
}

# 常量
_CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
    'tau': math.tau,
    'inf': math.inf,
}


def _safe_eval(expr):
    """
    安全地计算数学表达式

    Args:
        expr: 数学表达式字符串

    Returns:
        计算结果（float 或 int）

    Raises:
        ValueError: 表达式包含不支持的语法
    """
    try:
        tree = ast.parse(expr.strip(), mode='eval')
    except SyntaxError as e:
        raise ValueError(f"语法错误: {e}")

    return _eval_node(tree.body)


def _eval_node(node):
    """
    递归求值 AST 节点

    Args:
        node: AST 节点

    Returns:
        求值结果
    """
    # 数字常量
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    # 变量（常量 pi, e 等）
    if isinstance(node, ast.Name):
        if node.id in _CONSTANTS:
            return _CONSTANTS[node.id]
        raise ValueError(f"未知变量: {node.id}")

    # 二元运算：如 1 + 2
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _SUPPORTED_OPERATORS:
            raise ValueError(f"不支持的运算符: {op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _SUPPORTED_OPERATORS[op_type](left, right)

    # 一元运算：如 -x
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _SUPPORTED_OPERATORS:
            raise ValueError(f"不支持的一元运算符: {op_type.__name__}")
        operand = _eval_node(node.operand)
        return _SUPPORTED_OPERATORS[op_type](operand)

    # 函数调用：如 sqrt(2)
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in _SUPPORTED_FUNCTIONS:
                raise ValueError(f"不支持的函数: {func_name}")
            args = [_eval_node(arg) for arg in node.args]
            return _SUPPORTED_FUNCTIONS[func_name](*args)
        raise ValueError("不支持的函数调用方式")

    raise ValueError(f"不支持的表达式类型: {type(node).__name__}")


class CalculatorControl(BaseControl):
    """
    计算器控件
    对文本中每一行的数学表达式进行安全求值，将结果替换原内容
    """

    def __init__(self, parent=None):
        super().__init__("计算器", parent)

    def _init_content(self):
        layout = self.get_content_layout()

        grid_layout = QGridLayout()
        grid_layout.setSpacing(3)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # 第1行：保留小数位数
        prec_label = BodyLabel("保留小数位数:")
        prec_label.setAlignment( Qt.AlignVCenter)

        self.precision_input = LineEdit()
        self.precision_input.setPlaceholderText("2")
        self.precision_input.setText("2")
        self.precision_input.textChanged.connect(self._emit_parameters_changed)

        # 第2行: 强制保留小数位数
        always_prec_label = BodyLabel("总是显示小数位:")
        always_prec_label.setAlignment( Qt.AlignVCenter)

        self.always_prec = ComboBox()
        self.always_prec.addItems(["是", "否"])
        self.always_prec.setCurrentIndex(1)

        grid_layout.addWidget(prec_label, 0, 0)
        grid_layout.addWidget(self.precision_input, 0, 1)
        grid_layout.addWidget(always_prec_label, 1, 0)
        grid_layout.addWidget(self.always_prec, 1, 1)

        self.setMinimumHeight(120)

        layout.addLayout(grid_layout)

    def set_precision(self, precision):
        self.precision_input.setText(str(precision))

    def get_precision(self):
        text = self.precision_input.text().strip()
        if text.isdigit():
            return int(text)
        return 2

    def _format_number(self, value):
        """将数值格式化为字符串"""
        precision = self.get_precision()
        always = self.always_prec.currentIndex() == 0  # "是"

        if not always and isinstance(value, float) and value == int(value) and abs(value) < 1e15:
            return str(int(value))

        return f"{value:.{precision}f}"

    def execute(self, text):
        if not text:
            return text

        lines = text.split('\n')
        result_lines = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                result_lines.append(line)
                continue
            try:
                value = _safe_eval(stripped)
                result_lines.append(self._format_number(value))
            except (ValueError, Exception) as e:
                result_lines.append(f"[错误: {e}] {line}")
        return '\n'.join(result_lines)

    def reset_parameters(self):
        self.set_precision(2)
        self.always_prec.setCurrentIndex(1)

    def get_config(self):
        return {
            "type": "calculator",
            "precision": self.get_precision(),
            "always_prec": self.always_prec.currentIndex() == 0,
        }

    def load_config(self, config):
        if config.get("type") == "calculator":
            self.set_precision(config.get("precision", 2))
            self.always_prec.setCurrentIndex(0 if config.get("always_prec", False) else 1)

    def get_control_type(self):
        return "calculator"
