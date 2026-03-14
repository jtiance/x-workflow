# -*- coding: utf-8 -*-
"""
文本合并控件模块
提供按不同方式合并文本的功能
"""

from PySide6.QtWidgets import (QGridLayout, QLabel, QComboBox, QLineEdit, 
                              QCheckBox, QSizePolicy)
from PySide6.QtCore import Qt

from controls.base_control import BaseControl


SEPARATOR_MAP = {
    "无": "",
    "空格": " ",
    "逗号": ", ",
    "分号": "; ",
    "竖线": "| ",
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
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # 第1行：连接符
        join_label = QLabel("连接符:")
        join_label.setMinimumWidth(70)
        join_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.join_combo = QComboBox()
        self.join_combo.setEditable(False)
        self.join_combo.addItems(list(SEPARATOR_MAP.keys()))
        self.join_combo.setCurrentText("无")
        self.join_combo.currentTextChanged.connect(self._on_separator_changed)
        self.join_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.join_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(join_label, 0, 0)
        grid_layout.addWidget(self.join_combo, 0, 1)
        
        # 第2行：自定义连接符输入框
        self.custom_separator_input = QLineEdit()
        self.custom_separator_input.setPlaceholderText("请输入自定义连接符")
        self.custom_separator_input.setVisible(False)
        self.custom_separator_input.textChanged.connect(self._emit_parameters_changed)
        self.custom_separator_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(self.custom_separator_input, 1, 0, 1, 2)
        
        # 第3行：去除每行前后空白
        self.trim_checkbox = QCheckBox("去除每行前后空白")
        self.trim_checkbox.setChecked(True)
        self.trim_checkbox.stateChanged.connect(self._emit_parameters_changed)
        
        grid_layout.addWidget(self.trim_checkbox, 2, 0, 1, 2)  # 跨两列
        
        # 第4行：过滤空行
        self.filter_checkbox = QCheckBox("过滤空行")
        self.filter_checkbox.setChecked(True)
        self.filter_checkbox.stateChanged.connect(self._emit_parameters_changed)
        
        grid_layout.addWidget(self.filter_checkbox, 3, 0, 1, 2)  # 跨两列
        
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
        return separator.join(processed)
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.join_combo.setCurrentText("换行")
        self.custom_separator_input.setText("")
        self.custom_separator_input.setVisible(False)
        self.trim_checkbox.setChecked(True)
        self.filter_checkbox.setChecked(True)
        
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
            "filter_empty": self.filter_checkbox.isChecked()
        }
        
    def load_config(self, config):
        """
        加载控件配置
        
        Args:
            config: 控件配置字典
        """
        if config.get("type") == "text_merge":
            self.set_separator(config.get("separator", "\n"))
            self.trim_checkbox.setChecked(config.get("trim_whitespace", True))
            self.filter_checkbox.setChecked(config.get("filter_empty", True))
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "text_merge"
