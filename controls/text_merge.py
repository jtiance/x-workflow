# -*- coding: utf-8 -*-
"""
文本合并控件模块
提供按不同方式合并文本的功能
"""

from PySide6.QtWidgets import (QGridLayout, QLabel, QComboBox, QLineEdit, 
                              QCheckBox, QSizePolicy)
from PySide6.QtCore import Qt

from controls.base_control import BaseControl


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
        
        # 第1行：合并模式
        mode_label = QLabel("模式:")
        mode_label.setMinimumWidth(70)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["直接合并", "用连接符合并", "智能合并"])
        self.mode_combo.currentTextChanged.connect(self._on_mode_changed)
        self.mode_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.mode_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(mode_label, 0, 0)
        grid_layout.addWidget(self.mode_combo, 0, 1)
        
        # 第2行：连接符
        join_label = QLabel("连接符:")
        join_label.setMinimumWidth(70)
        
        self.join_combo = QComboBox()
        self.join_combo.setEditable(True)
        self.join_combo.addItems(["", " ", "\\n", ", ", "; ", "| "])
        self.join_combo.setCurrentText("\\n")
        self.join_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.join_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(join_label, 1, 0)
        grid_layout.addWidget(self.join_combo, 1, 1)
        
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
        
        # 保存引用以便控制显隐
        self.join_label_widget = join_label
        self.join_combo_widget = self.join_combo
        
        # 初始状态：默认用连接符合并，显示连接符
        self._on_mode_changed("用连接符合并")
        
        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)
        
        # 将GridLayout添加到内容布局
        layout.addLayout(grid_layout)
    
    def _on_mode_changed(self, mode_text):
        """合并模式改变时的处理"""
        if mode_text == "直接合并":
            self.join_label_widget.hide()
            self.join_combo_widget.hide()
        else:
            self.join_label_widget.show()
            self.join_combo_widget.show()
    
    def get_merge_mode(self):
        """
        获取当前合并模式
        
        Returns:
            str: 合并模式
        """
        mode_text = self.mode_combo.currentText()
        if mode_text == "直接合并":
            return "direct"
        elif mode_text == "用连接符合并":
            return "join"
        else:
            return "smart"
    
    def get_separator(self):
        """
        获取当前连接符
        
        Returns:
            str: 连接符
        """
        sep = self.join_combo.currentText()
        # 处理转义字符
        if sep == "\\n":
            return "\n"
        elif sep == "\\t":
            return "\t"
        return sep
    
    def set_separator(self, separator):
        """
        设置连接符
        
        Args:
            separator: 连接符
        """
        # 处理转义字符
        if separator == "\n":
            self.join_combo.setCurrentText("\\n")
        elif separator == "\t":
            self.join_combo.setCurrentText("\\t")
        else:
            self.join_combo.setCurrentText(separator)
    
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
        
        mode = self.get_merge_mode()
        separator = self.get_separator()
        
        if mode == "direct":
            return "".join(processed)
        elif mode == "join":
            return separator.join(processed)
        else:
            # 智能合并
            result = []
            for i, line in enumerate(processed):
                result.append(line)
                if i < len(processed) - 1 and separator:
                    result.append(separator)
            return "".join(result)
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.mode_combo.setCurrentText("用连接符合并")
        self.join_combo.setCurrentText("\\n")
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
            "merge_mode": self.get_merge_mode(),
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
            merge_mode = config.get("merge_mode", "join")
            if merge_mode == "direct":
                self.mode_combo.setCurrentText("直接合并")
            elif merge_mode == "join":
                self.mode_combo.setCurrentText("用连接符合并")
            else:
                self.mode_combo.setCurrentText("智能合并")
            self.set_separator(config.get("separator", "\\n"))
            self.trim_checkbox.setChecked(config.get("trim_whitespace", True))
            self.filter_checkbox.setChecked(config.get("filter_empty", True))
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "text_merge"
