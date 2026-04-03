# -*- coding: utf-8 -*-
"""
文本合并控件模块
提供按不同方式合并文本的功能
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QGridLayout, QSizePolicy)
from qfluentwidgets import ComboBox, BodyLabel, LineEdit, SpinBox, SwitchButton, TogglePushButton

from controls.base_control import BaseControl

SEPARATOR_MAP = {
    "无": "",
    "空格": " ",
    "逗号 ( , )": ",",
    "分号 ( ; )": ";",
    "竖线 ( | )": "|",
    "制表符 (\\t)": "\t",
    "自定义": None
}


class TextMergeControl(BaseControl):
    """
    文本合并控件类
    提供按不同方式合并文本的功能
    """

    def __init__(self, parent=None):
        """
        初始化文本合并控件

        Args:
            parent: 父控件
        """
        super().__init__("文本合并", parent)

    def _init_content(self):
        """
        初始化内容区域
        添加文本合并相关的控件
        """
        layout = self.get_content_layout()

        # 使用GridLayout确保对齐
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # 第1行：连接符
        join_label = BodyLabel("连接符:")
        join_label.setMinimumWidth(70)
        join_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.join_combo = ComboBox()
        self.join_combo.addItems(list(SEPARATOR_MAP.keys()))
        self.join_combo.setCurrentText("无")
        self.join_combo.currentTextChanged.connect(self._on_separator_changed)
        self.join_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.join_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        grid_layout.addWidget(join_label, 0, 0)
        grid_layout.addWidget(self.join_combo, 0, 1)

        # 第2行：自定义连接符输入框
        self.custom_separator_input = LineEdit()
        self.custom_separator_input.setPlaceholderText("请输入自定义连接符")
        self.custom_separator_input.setVisible(False)
        self.custom_separator_input.textChanged.connect(self._emit_parameters_changed)
        self.custom_separator_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        grid_layout.addWidget(self.custom_separator_input, 1, 1)  # 放在第二列

        # 第3行：按钮组
        from PySide6.QtWidgets import QHBoxLayout

        # 创建水平布局容纳2个按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)

        # 去除每行前后空白按钮
        self.trim_checkbox = TogglePushButton("删除空白")
        self.trim_checkbox.setChecked(False)
        self.trim_checkbox.setToolTip("删除文本前后的空白字符")
        self.trim_checkbox.clicked.connect(self._emit_parameters_changed)
        self.trim_checkbox.setFixedWidth(90)

        # 过滤空行按钮
        self.filter_checkbox = TogglePushButton("忽略空行")
        self.filter_checkbox.setChecked(True)
        self.filter_checkbox.setToolTip("空行不增加额外连接符")
        self.filter_checkbox.clicked.connect(self._emit_parameters_changed)
        self.filter_checkbox.setFixedWidth(90)

        # 添加按钮到水平布局
        button_layout.addWidget(self.trim_checkbox)
        button_layout.addWidget(self.filter_checkbox)
        button_layout.addStretch()  # 右侧添加弹性空间

        # 将水平布局添加到网格布局
        grid_layout.addLayout(button_layout, 2, 1)  # 放在第二列

        # 第4行：支持换行开关
        enable_line_break_label = BodyLabel("按字符数量换行:")
        enable_line_break_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.enable_line_break_switch = SwitchButton()
        self.enable_line_break_switch.setChecked(False)  # 默认关闭
        self.enable_line_break_switch.checkedChanged.connect(self._on_line_break_changed)
        self.enable_line_break_switch.setOffText("关闭")
        self.enable_line_break_switch.setOnText("开启")

        grid_layout.addWidget(enable_line_break_label, 3, 0)
        grid_layout.addWidget(self.enable_line_break_switch, 3, 1, 1, 1, Qt.AlignLeft)  # 左对齐

        # 第5行：最大字符数
        max_chars_label = BodyLabel("最大字符数:")
        max_chars_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.max_chars_spin = SpinBox()
        # 先设置范围，再设置值
        self.max_chars_spin.setMinimum(0)  # 0表示不限制
        self.max_chars_spin.setMaximum(1000000)  # 最大100万
        self.max_chars_spin.setSingleStep(10000)  # 步宽10000
        self.max_chars_spin.setValue(10000)  # 默认值
        self.max_chars_spin.setSuffix("字符")  # 后缀
        self.max_chars_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.max_chars_spin.valueChanged.connect(self._emit_parameters_changed)
        self.max_chars_spin.setEnabled(False)  # 默认禁用（因为开关默认关闭）

        grid_layout.addWidget(max_chars_label, 4, 0)
        grid_layout.addWidget(self.max_chars_spin, 4, 1)  # 左对齐

        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)

        # 将GridLayout添加到内容布局
        layout.addLayout(grid_layout)

    def _on_separator_changed(self, display_text):
        """
        当连接符选项改变时调用
        """
        if display_text == "自定义":
            self.custom_separator_input.setVisible(True)
        else:
            self.custom_separator_input.setVisible(False)

    def _on_line_break_changed(self, checked):
        """
        当换行开关改变时调用

        Args:
            checked: 是否开启
        """
        # 启用或禁用最大字符数输入框
        self.max_chars_spin.setEnabled(checked)
        # 发出参数改变信号
        self._emit_parameters_changed()

    def get_separator(self):
        """
        获取当前连接符

        Returns:
            str: 连接符
        """
        display_text = self.join_combo.currentText()

        if display_text == "自定义":
            return self.custom_separator_input.text()

        return SEPARATOR_MAP.get(display_text, "\n")

    def set_separator(self, separator):
        """
        设置连接符

        Args:
            separator: 连接符
        """
        found = False
        for display_name, actual_sep in SEPARATOR_MAP.items():
            if actual_sep == separator:
                self.join_combo.setCurrentText(display_name)
                found = True
                break

        if not found:
            self.join_combo.setCurrentText("自定义")
            self.custom_separator_input.setText(separator)
            self.custom_separator_input.setVisible(True)

    def get_max_chars(self):
        """
        获取最大字符数

        Returns:
            int: 最大字符数，0表示不限制
        """
        return self.max_chars_spin.value()

    def set_max_chars(self, value):
        """
        设置最大字符数

        Args:
            value: 最大字符数
        """
        self.max_chars_spin.setValue(value)

    def is_enable_line_break(self):
        """
        获取是否启用换行功能

        Returns:
            bool: 是否启用换行
        """
        return self.enable_line_break_switch.isChecked()

    def set_enable_line_break(self, enabled):
        """
        设置是否启用换行功能

        Args:
            enabled: 是否启用换行
        """
        self.enable_line_break_switch.setChecked(enabled)
        # 同时启用或禁用 SpinBox
        self.max_chars_spin.setEnabled(enabled)

    def set_disabled_state(self, disabled):
        """
        重写父类方法，处理 max_chars_spin 的特殊情况

        Args:
            disabled: 是否禁用
        """
        # 调用父类方法处理通用的禁用逻辑
        super().set_disabled_state(disabled)

        # 对于 max_chars_spin，需要同时考虑控件禁用状态和换行开关状态
        # 如果控件被禁用，则禁用 SpinBox
        # 如果控件被启用，则根据换行开关状态决定
        if disabled:
            self.max_chars_spin.setEnabled(False)
        else:
            self.max_chars_spin.setEnabled(self.enable_line_break_switch.isChecked())

    def execute(self, text):
        """
        执行文本合并操作（按行分割后再合并）

        Args:
            text: 要处理的文本

        Returns:
            str: 处理后的文本
        """
        # 按行分割
        lines = text.splitlines()

        # 预处理
        processed = []
        for line in lines:
            if self.trim_checkbox.isChecked():
                line = line.strip()
            if self.filter_checkbox.isChecked() and not line:
                continue
            processed.append(line)

        if not processed:
            return ""

        separator = self.get_separator()
        max_chars = self.get_max_chars()
        enable_line_break = self.is_enable_line_break()

        # 如果启用了换行功能且设置了最大字符数限制
        if enable_line_break and max_chars > 0:
            result_lines = []
            current_line = ""

            for line in processed:
                # 如果是第一行，直接添加
                if not current_line:
                    current_line = line
                else:
                    # 检查添加后是否超过限制
                    if len(current_line) + len(separator) + len(line) <= max_chars:
                        current_line += separator + line
                    else:
                        # 超过限制，保存当前行，开始新行
                        result_lines.append(current_line)
                        current_line = line

            # 添加最后一行
            if current_line:
                result_lines.append(current_line)

            return "\n".join(result_lines)
        else:
            # 没有限制或未启用换行，直接合并
            return separator.join(processed)

    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.join_combo.setCurrentText("换行")
        self.custom_separator_input.setText("")
        self.custom_separator_input.setVisible(False)
        self.trim_checkbox.setChecked(False)
        self.filter_checkbox.setChecked(True)
        self.enable_line_break_switch.setChecked(False)  # 默认关闭
        self.max_chars_spin.setValue(10000)
        self.max_chars_spin.setEnabled(False)  # 因为开关默认关闭，所以禁用 SpinBox

    def get_config(self):
        """
        获取控件配置

        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "text_merge",
            "separator": self.get_separator(),
            "trim_whitespace": self.trim_checkbox.isChecked(),
            "filter_empty": self.filter_checkbox.isChecked(),
            "enable_line_break": self.is_enable_line_break(),
            "max_chars": self.get_max_chars()
        }

    def load_config(self, config):
        """
        加载控件配置

        Args:
            config: 控件配置字典
        """
        if config.get("type") == "text_merge":
            self.set_separator(config.get("separator", "\n"))
            self.trim_checkbox.setChecked(config.get("trim_whitespace", False))
            self.filter_checkbox.setChecked(config.get("filter_empty", True))
            self.set_enable_line_break(config.get("enable_line_break", False))
            self.set_max_chars(config.get("max_chars", 10000))

    def get_control_type(self):
        """
        获取控件类型

        Returns:
            str: 控件类型标识
        """
        return "text_merge"
