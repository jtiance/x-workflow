# -*- coding: utf-8 -*-
"""
HTML格式化控件模块
提供HTML格式化功能的可视化控件
"""

import re

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QSizePolicy
from qfluentwidgets import BodyLabel, SpinBox

from controls.base_control import BaseControl


class HtmlFormatControl(BaseControl):
    """
    HTML格式化控件
    用于格式化HTML文本
    """

    def __init__(self, parent=None):
        """
        初始化HTML格式化控件

        Args:
            parent: 父控件
        """
        super().__init__("HTML格式化", parent)

    def _init_content(self):
        """
        初始化内容区域
        添加HTML格式化相关的控件
        """
        layout = self.get_content_layout()

        # 使用GridLayout确保对齐
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # 第1行：缩进
        indent_label = BodyLabel("缩进:")
        indent_label.setMinimumWidth(70)
        indent_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.indent_spin = SpinBox()
        self.indent_spin.setMinimum(0)
        self.indent_spin.setMaximum(8)
        self.indent_spin.setValue(2)
        self.indent_spin.setSuffix(" 空格")
        self.indent_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.indent_spin.valueChanged.connect(self._emit_parameters_changed)

        grid_layout.addWidget(indent_label, 0, 0)
        grid_layout.addWidget(self.indent_spin, 0, 1)

        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)

        # 将GridLayout添加到内容布局
        layout.addLayout(grid_layout)

    def get_indent(self):
        """
        获取缩进设置

        Returns:
            int: 缩进空格数，0表示不缩进
        """
        return self.indent_spin.value()

    def set_indent(self, indent):
        """
        设置缩进

        Args:
            indent: 缩进空格数
        """
        self.indent_spin.setValue(indent)

    def execute(self, text):
        """
        执行HTML格式化操作

        Args:
            text: 要处理的文本

        Returns:
            str: 处理后的文本
        """
        # 获取设置
        indent = self.get_indent()

        # 格式化HTML
        formatted = self._format_html(text, indent)

        return formatted

    def _format_html(self, html_string, indent):
        """
        格式化HTML字符串

        Args:
            html_string: HTML字符串
            indent: 缩进空格数

        Returns:
            str: 格式化后的HTML字符串
        """
        if indent <= 0:
            return html_string

        # 使用BeautifulSoup或类似库会更好，但为了减少依赖，使用简单实现
        # 这里使用基于标签的简化格式化

        # 规范化：在标签后添加换行
        formatted = re.sub(r'>\s*<', '>\n<', html_string)
        formatted = re.sub(r'>\s*$', '>', formatted)

        # 按行处理
        lines = formatted.split('\n')
        result = []
        indent_level = 0
        indent_str = ' ' * indent

        # 需要增加缩进的标签
        self_closing_tags = ['</', ]
        # 不增加缩进的标签（自闭合标签）
        self_closing_tags = [
            '<br', '<hr', '<img', '<input', '<meta', '<link',
            '<!DOCTYPE', '<!--', '-->', '<base', '<area', '<col',
            '<frame', '<param'
        ]

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 检查是否是闭合标签
            is_closing = line.startswith('</')

            # 检查是否是自闭合标签
            is_self_closing = any(tag in line for tag in self_closing_tags)

            # 调整缩进级别
            if is_closing:
                indent_level = max(0, indent_level - 1)

            # 添加缩进
            if indent > 0:
                result.append(indent_str * indent_level + line)
            else:
                result.append(line)

            # 如果不是闭合标签且不是自闭合标签，增加缩进级别
            if not is_closing and not is_self_closing:
                indent_level += 1

        return '\n'.join(result)

    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.set_indent(2)

    def get_config(self):
        """
        获取控件配置

        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "html_format",
            "indent": self.get_indent()
        }

    def load_config(self, config):
        """
        加载控件配置

        Args:
            config: 控件配置字典
        """
        if config.get("type") == "html_format":
            self.set_indent(config.get("indent", 2))

    def get_control_type(self):
        """
        获取控件类型

        Returns:
            str: 控件类型标识
        """
        return "html_format"