# -*- coding: utf-8 -*-
"""
Excel转JSON控件模块
提供将Excel文件转换为JSON格式的功能
"""

import polars as pl
import json
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QSizePolicy, QHBoxLayout
from qfluentwidgets import ComboBox, BodyLabel, SpinBox, TogglePushButton

from components.custom_file import CustomFile
from controls.base_control import BaseControl


class ExcelToJsonControl(BaseControl):
    """
    Excel转JSON控件类
    将Excel文件内容转换为JSON格式输出
    """

    def __init__(self, parent=None):
        """
        初始化Excel转JSON控件

        Args:
            parent: 父控件
        """
        super().__init__("Excel转JSON", parent)

    def _init_content(self):
        """
        初始化内容区域
        添加Excel转JSON相关的控件
        """
        layout = self.get_content_layout()

        # 使用GridLayout确保对齐
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # 第1行：Excel文件选择（参照ReadExcelColumnControl的第一行）
        excel_label = BodyLabel("Excel:")
        excel_label.setMinimumWidth(90)
        excel_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.excel_file = CustomFile()
        self.excel_file.set_file_filters(["xlsx", "xls", "csv"])
        self.excel_file.setPlaceholderText("请选择Excel文件")
        self.excel_file.textChanged.connect(self._emit_parameters_changed)
        self.excel_file.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        grid_layout.addWidget(excel_label, 0, 0)
        grid_layout.addWidget(self.excel_file, 0, 1)

        # 第2行：缩进（参照JsonFormatControl的第一行）
        indent_label = BodyLabel("JSON缩进:")
        indent_label.setMinimumWidth(90)
        indent_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.indent_spin = SpinBox()
        self.indent_spin.setMinimum(0)
        self.indent_spin.setMaximum(8)
        self.indent_spin.setValue(4)
        self.indent_spin.setSuffix(" 空格")
        self.indent_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.indent_spin.valueChanged.connect(self._emit_parameters_changed)

        grid_layout.addWidget(indent_label, 1, 0)
        grid_layout.addWidget(self.indent_spin, 1, 1)

        # 第3行：按键名排序和确保ASCII（同一列中并列排放）
        # 创建水平布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)  # 设置按钮间距
        button_layout.setAlignment(Qt.AlignLeft)  # 设置按钮靠左对齐

        # 按键名排序
        self.sort_checkbox = TogglePushButton("排序")
        self.sort_checkbox.setChecked(False)
        self.sort_checkbox.setToolTip("按键名排序")
        self.sort_checkbox.clicked.connect(self._emit_parameters_changed)
        self.sort_checkbox.setFixedWidth(60)
        button_layout.addWidget(self.sort_checkbox)

        # 确保ASCII
        self.ascii_checkbox = TogglePushButton("ASCII")
        self.ascii_checkbox.setChecked(False)
        self.ascii_checkbox.setToolTip("确保ASCII（转义非ASCII字符）")
        self.ascii_checkbox.clicked.connect(self._emit_parameters_changed)
        self.ascii_checkbox.setFixedWidth(60)
        button_layout.addWidget(self.ascii_checkbox)

        # 在按钮右侧添加弹性空间，确保按钮靠左对齐
        button_layout.addStretch()

        # 将水平布局添加到网格布局的同一列
        grid_layout.addLayout(button_layout, 2, 1)  # 放在第3行第2列

        # 第4行：输出格式
        format_label = BodyLabel("输出格式:")
        format_label.setMinimumWidth(90)
        format_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.format_combo = ComboBox()
        self.format_combo.addItems(["数组格式", "对象数组格式"])
        self.format_combo.setCurrentText("对象数组格式")
        self.format_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.format_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        grid_layout.addWidget(format_label, 3, 0)
        grid_layout.addWidget(self.format_combo, 3, 1)

        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)

        # 将GridLayout添加到内容布局
        layout.addLayout(grid_layout)

    def execute(self, text):
        """
        执行控件核心逻辑
        读取Excel文件，转换为JSON格式输出

        Args:
            text: 输入文本（本控件不使用输入文本）

        Returns:
            str: 处理后的JSON文本
        """
        file_path = self.excel_file.text().strip()
        if not file_path:
            return ""

        try:
            # 读取文件
            if file_path.endswith('.csv'):
                df = pl.read_csv(file_path)
            else:
                df = pl.read_excel(file_path)

            # 转换为字典列表
            data = df.to_dicts()

            # 获取设置
            indent = self.indent_spin.value()
            sort_keys = self.sort_checkbox.isChecked()
            ensure_ascii = self.ascii_checkbox.isChecked()
            output_format = self.format_combo.currentText()

            # 处理输出格式
            if output_format == "数组格式":
                # 转换为列数组格式
                col_data = {}
                for col in df.columns:
                    col_data[col] = df[col].to_list()
                data = col_data

            # 格式化JSON
            formatted = json.dumps(
                data,
                indent=indent if indent > 0 else None,
                sort_keys=sort_keys,
                ensure_ascii=ensure_ascii
            )

            return formatted

        except Exception as e:
            return f"转换Excel到JSON失败: {str(e)}"

    def get_config(self):
        """
        获取控件配置
        注意：不包含文件路径

        Returns:
            dict: 配置字典
        """
        return {
            "indent": self.indent_spin.value(),
            "sort_keys": self.sort_checkbox.isChecked(),
            "ensure_ascii": self.ascii_checkbox.isChecked(),
            "output_format": self.format_combo.currentText()
        }

    def load_config(self, config):
        """
        加载控件配置

        Args:
            config: 配置字典
        """
        # 加载缩进配置
        indent = config.get("indent", 4)
        self.indent_spin.setValue(indent)

        # 加载排序配置
        sort_keys = config.get("sort_keys", False)
        self.sort_checkbox.setChecked(sort_keys)

        # 加载ASCII配置
        ensure_ascii = config.get("ensure_ascii", False)
        self.ascii_checkbox.setChecked(ensure_ascii)

        # 加载输出格式配置
        output_format = config.get("output_format", "对象数组格式")
        if output_format in ["数组格式", "对象数组格式"]:
            self.format_combo.setCurrentText(output_format)
        else:
            self.format_combo.setCurrentText("对象数组格式")

    def get_control_type(self):
        """
        获取控件类型标识

        Returns:
            str: 控件类型字符串
        """
        return "excel_to_json"

    def reset_parameters(self):
        """重置参数为默认值"""
        # 清空文件选择
        self.excel_file.clear()

        # 重置缩进
        self.indent_spin.setValue(4)

        # 重置复选框
        self.sort_checkbox.setChecked(False)
        self.ascii_checkbox.setChecked(False)

        # 重置输出格式
        self.format_combo.setCurrentText("对象数组格式")
