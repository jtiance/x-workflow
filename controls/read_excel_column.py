# -*- coding: utf-8 -*-
"""
读取Excel列控件模块
提供读取Excel文件列信息并转换为文本输出的功能
"""

import polars as pl
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QGridLayout, QSizePolicy, QScrollArea, QWidget, QHBoxLayout)
from qfluentwidgets import ComboBox, BodyLabel, LineEdit, TogglePushButton

from components.custom_file import CustomFile
from controls.base_control import BaseControl

SEPARATOR_MAP = {
    "无": "",
    "空格": " ",
    "逗号 ( , )": ",",
    "分号 ( ; )": ";",
    "竖线 ( | )": "|",
    "制表符 ( \\t )": "\t",
    "自定义": None
}


class ReadExcelColumnControl(BaseControl):
    """
    读取Excel列控件类
    读取Excel文件的指定列，按分隔符连接后输出文本
    """

    def __init__(self, parent=None):
        """
        初始化读取Excel列控件

        Args:
            parent: 父控件
        """
        super().__init__("读取Excel列", parent)

    def _init_content(self):
        """
        初始化内容区域
        添加读取Excel列相关的控件
        """
        layout = self.get_content_layout()

        # 使用GridLayout确保对齐
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # 第1行：Excel文件选择
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

        # 第2行：选择列
        column_label = BodyLabel("选择列:")
        column_label.setMinimumWidth(90)
        column_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        scroll_area.setFixedHeight(48)  # 增加高度，为滚动条留出空间
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea QWidget {
                background: transparent;
            }
            QScrollBar:horizontal {
                height: 6px;
                background: #2a2a2a;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #555555;
                border-radius: 3px;
                min-width: 20px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
                height: 0px;
            }
        """)

        # 创建滚动区域内容
        scroll_content = QWidget()
        scroll_layout = QHBoxLayout(scroll_content)
        scroll_layout.setSpacing(3)
        scroll_layout.setContentsMargins(2, 2, 2, 8)  # 增加底部边距，避免滚动条盖住按钮

        # 创建26个列选择按钮 A-Z
        self.column_buttons = []
        for i in range(26):
            col_char = chr(ord('A') + i)
            btn = TogglePushButton(col_char)
            btn.setFixedSize(38, 30)
            btn.clicked.connect(self._emit_parameters_changed)
            self.column_buttons.append(btn)
            scroll_layout.addWidget(btn)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)

        grid_layout.addWidget(column_label, 1, 0)
        grid_layout.addWidget(scroll_area, 1, 1)

        # 第3行：列间分隔符
        separator_label = BodyLabel("列间分隔符:")
        separator_label.setMinimumWidth(90)
        separator_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.separator_combo = ComboBox()
        self.separator_combo.addItems(list(SEPARATOR_MAP.keys()))
        self.separator_combo.setCurrentText("无")
        self.separator_combo.currentTextChanged.connect(self._on_separator_changed)
        self.separator_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.separator_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        grid_layout.addWidget(separator_label, 2, 0)
        grid_layout.addWidget(self.separator_combo, 2, 1)

        # 第4行：自定义分隔符输入框
        self.custom_separator_input = LineEdit()
        self.custom_separator_input.setPlaceholderText("请输入自定义分隔符")
        self.custom_separator_input.setVisible(False)
        self.custom_separator_input.textChanged.connect(self._emit_parameters_changed)
        self.custom_separator_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        grid_layout.addWidget(self.custom_separator_input, 3, 1)

        # 将网格布局添加到主布局
        layout.addLayout(grid_layout)

    def _on_separator_changed(self):
        """分隔符选择变化处理"""
        # 显示/隐藏自定义分隔符输入框
        is_custom = self.separator_combo.currentText() == "自定义"
        self.custom_separator_input.setVisible(is_custom)

    def _get_separator(self):
        """获取当前选中的分隔符"""
        selected = self.separator_combo.currentText()
        if selected == "自定义":
            return self.custom_separator_input.text()
        return SEPARATOR_MAP.get(selected, "")

    def _get_selected_columns(self):
        """获取选中的列索引列表"""
        selected = []
        for idx, btn in enumerate(self.column_buttons):
            if btn.isChecked():
                selected.append(idx)
        return selected

    def execute(self, text):
        """
        执行控件核心逻辑
        读取Excel文件，选择指定列，按分隔符连接后输出

        Args:
            text: 输入文本（本控件不使用输入文本）

        Returns:
            str: 处理后的文本，每行对应Excel的一行数据
        """
        file_path = self.excel_file.text().strip()
        if not file_path:
            return ""

        # 获取选中的列
        selected_cols = self._get_selected_columns()
        if not selected_cols:
            return ""

        separator = self._get_separator()

        try:
            # 读取文件
            if file_path.endswith('.csv'):
                df = pl.read_csv(file_path)
            else:
                df = pl.read_excel(file_path)

            # 选择指定列
            selected_col_names = [df.columns[i] for i in selected_cols if i < len(df.columns)]
            if not selected_col_names:
                return ""

            df_selected = df.select(selected_col_names)

            # 转换为文本行
            lines = []
            for row in df_selected.iter_rows():
                # 将行数据转换为字符串并连接
                str_row = [str(item) if item is not None else "" for item in row]
                lines.append(separator.join(str_row))

            return "\n".join(lines)

        except Exception as e:
            return f"读取Excel文件失败: {str(e)}"

    def get_config(self):
        """
        获取控件配置
        注意：不包含文件路径

        Returns:
            dict: 配置字典
        """
        return {
            "selected_columns": self._get_selected_columns(),
            "separator": self.separator_combo.currentText(),
            "custom_separator": self.custom_separator_input.text()
        }

    def load_config(self, config):
        """
        加载控件配置

        Args:
            config: 配置字典
        """
        # 加载选中的列
        selected_cols = config.get("selected_columns", [])
        for idx, btn in enumerate(self.column_buttons):
            btn.setChecked(idx in selected_cols)

        # 加载分隔符配置
        separator = config.get("separator", "无")
        if separator in SEPARATOR_MAP:
            self.separator_combo.setCurrentText(separator)
        else:
            self.separator_combo.setCurrentText("无")

        # 加载自定义分隔符
        custom_sep = config.get("custom_separator", "")
        self.custom_separator_input.setText(custom_sep)

        # 触发分隔符变化事件，更新UI
        self._on_separator_changed()

    def get_control_type(self):
        """
        获取控件类型标识

        Returns:
            str: 控件类型字符串
        """
        return "read_excel_column"

    def reset_parameters(self):
        """重置参数为默认值"""
        # 清空文件选择
        self.excel_file.clear()

        # 取消所有列选择
        for btn in self.column_buttons:
            btn.setChecked(False)

        # 重置分隔符
        self.separator_combo.setCurrentText("无")
        self.custom_separator_input.clear()
