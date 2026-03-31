# -*- coding: utf-8 -*-
"""
XML格式化控件模块
提供XML格式化功能的可视化控件
"""

from xml.dom import minidom

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QSizePolicy
from qfluentwidgets import BodyLabel, SpinBox

from controls.base_control import BaseControl


class XmlFormatControl(BaseControl):
    """
    XML格式化控件
    用于格式化XML文本
    """

    def __init__(self, parent=None):
        """
        初始化XML格式化控件

        Args:
            parent: 父控件
        """
        super().__init__("XML格式化", parent)

    def _init_content(self):
        """
        初始化内容区域
        添加XML格式化相关的控件
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
        执行XML格式化操作

        Args:
            text: 要处理的文本

        Returns:
            str: 处理后的文本
        """
        # 获取设置
        indent = self.get_indent()

        # 格式化XML
        formatted = self._format_xml(text, indent)

        return formatted

    def _format_xml(self, xml_string, indent):
        """
        格式化XML字符串

        Args:
            xml_string: XML字符串
            indent: 缩进空格数

        Returns:
            str: 格式化后的XML字符串
        """
        try:
            # 解析XML
            dom = minidom.parseString(xml_string)

            # 格式化
            if indent > 0:
                # 使用minidom的toprettyxml方法进行格式化
                formatted = dom.toprettyxml(indent=' ' * indent)
            else:
                # 不缩进
                formatted = dom.toxml()

            # 移除XML声明（如果存在）
            if formatted.startswith('<?xml'):
                formatted = formatted.split('\n', 1)[1] if '\n' in formatted else formatted.split('?>', 1)[1]
                formatted = formatted.lstrip()

            return formatted

        except Exception as e:
            # 如果解析失败，尝试简单的缩进格式化
            return self._simple_format_xml(xml_string, indent)

    def _simple_format_xml(self, xml_string, indent):
        """
        简单的XML格式化（当正常解析失败时使用）

        Args:
            xml_string: XML字符串
            indent: 缩进空格数

        Returns:
            str: 格式化后的XML字符串
        """
        if indent <= 0:
            return xml_string

        # 简单的基于标签的格式化
        import re
        pattern = re.compile(r'(</?[\w\-:]+>)')
        result = []
        indent_level = 0
        indent_str = ' ' * indent

        for line in xml_string.split('\n'):
            line = line.strip()
            if not line:
                continue

            if line.startswith('</'):
                indent_level = max(0, indent_level - 1)
                result.append(indent_str * indent_level + line)
            elif line.startswith('<') and not line.startswith('</') and '>' in line and not line.endswith('/>'):
                result.append(indent_str * indent_level + line)
                indent_level += 1
            else:
                result.append(indent_str * indent_level + line)

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
            "type": "xml_format",
            "indent": self.get_indent()
        }

    def load_config(self, config):
        """
        加载控件配置

        Args:
            config: 控件配置字典
        """
        if config.get("type") == "xml_format":
            self.set_indent(config.get("indent", 2))

    def get_control_type(self):
        """
        获取控件类型

        Returns:
            str: 控件类型标识
        """
        return "xml_format"