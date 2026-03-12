# -*- coding: utf-8 -*-
"""
文本分割控件模块
提供按不同方式分割文本的功能
"""

from PySide6.QtWidgets import (QGridLayout, QLabel, QComboBox, QLineEdit, 
                              QSpinBox, QSizePolicy)
from PySide6.QtCore import Qt

from controls.base_control import BaseControl


class TextSplitControl(BaseControl):
    """
    文本分割控件类
    提供按行、分隔符、长度等方式分割文本功能
    """
    
    def __init__(self, parent=None):
        """
        初始化文本分割控件
        
        Args:
            parent: 父控件
        """
        super().__init__("文本分割", parent)
        
    def _init_content(self):
        """
        初始化内容区域
        添加文本分割相关的控件
        """
        layout = self.get_content_layout()
        
        # 使用GridLayout确保对齐
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # 第1行：分割模式
        mode_label = QLabel("模式:")
        mode_label.setMinimumWidth(70)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["按分隔符分割", "按长度分割"])
        self.mode_combo.currentTextChanged.connect(self._on_mode_changed)
        self.mode_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.mode_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(mode_label, 0, 0)
        grid_layout.addWidget(self.mode_combo, 0, 1)
        
        # 第2行：分隔符
        delimiter_label = QLabel("分隔符:")
        delimiter_label.setMinimumWidth(70)
        
        self.delimiter_combo = QComboBox()
        self.delimiter_combo.setEditable(True)
        self.delimiter_combo.addItems([",", ";", "|", " ", "\t"])
        self.delimiter_combo.setCurrentText(",")
        self.delimiter_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.delimiter_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(delimiter_label, 1, 0)
        grid_layout.addWidget(self.delimiter_combo, 1, 1)
        
        # 第3行：字符数
        length_label = QLabel("字符数:")
        length_label.setMinimumWidth(70)
        
        self.length_spin = QSpinBox()
        self.length_spin.setMinimum(1)
        self.length_spin.setMaximum(10000)
        self.length_spin.setValue(10)
        self.length_spin.valueChanged.connect(self._emit_parameters_changed)
        self.length_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(length_label, 2, 0)
        grid_layout.addWidget(self.length_spin, 2, 1)
        
        # 保存引用以便控制显隐
        self.delimiter_label = delimiter_label
        self.delimiter_combo_widget = self.delimiter_combo
        self.length_label = length_label
        self.length_spin_widget = self.length_spin
        
        # 初始状态：显示分隔符，隐藏长度
        length_label.hide()
        self.length_spin.hide()
        
        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)
        
        # 将GridLayout添加到内容布局
        layout.addLayout(grid_layout)
    
    def _on_mode_changed(self, mode_text):
        """分割模式改变时的处理"""
        if mode_text == "按分隔符分割":
            self.delimiter_label.show()
            self.delimiter_combo_widget.show()
            self.length_label.hide()
            self.length_spin_widget.hide()
        elif mode_text == "按长度分割":
            self.delimiter_label.hide()
            self.delimiter_combo_widget.hide()
            self.length_label.show()
            self.length_spin_widget.show()
    
    def get_split_mode(self):
        """
        获取当前分割模式
        
        Returns:
            str: 分割模式 ('delimiter' 或 'length')
        """
        mode_text = self.mode_combo.currentText()
        if mode_text == "按分隔符分割":
            return "delimiter"
        else:
            return "length"
    
    def get_delimiter(self):
        """
        获取当前分隔符
        
        Returns:
            str: 分隔符
        """
        return self.delimiter_combo.currentText()
    
    def get_split_length(self):
        """
        获取当前分割长度
        
        Returns:
            int: 分割长度
        """
        return self.length_spin.value()
    
    def set_delimiter(self, delimiter):
        """
        设置分隔符
        
        Args:
            delimiter: 分隔符
        """
        self.delimiter_combo.setCurrentText(delimiter)
    
    def execute(self, text):
        """
        执行文本分割操作
        
        Args:
            text: 要处理的文本
            
        Returns:
            str: 处理后的文本（用换行符连接）
        """
        mode = self.get_split_mode()
        
        if mode == "delimiter":
            delimiter = self.get_delimiter()
            parts = text.split(delimiter)
            return "\n".join(parts)
        elif mode == "length":
            length = self.get_split_length()
            result = []
            for i in range(0, len(text), length):
                result.append(text[i:i + length])
            return "\n".join(result)
        
        return text
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.mode_combo.setCurrentText("按分隔符分割")
        self.delimiter_combo.setCurrentText(",")
        self.length_spin.setValue(10)
        
    def get_config(self):
        """
        获取控件配置
        
        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "text_split",
            "split_mode": self.get_split_mode(),
            "delimiter": self.get_delimiter(),
            "split_length": self.get_split_length()
        }
        
    def load_config(self, config):
        """
        加载控件配置
        
        Args:
            config: 控件配置字典
        """
        if config.get("type") == "text_split":
            split_mode = config.get("split_mode", "delimiter")
            if split_mode == "delimiter":
                self.mode_combo.setCurrentText("按分隔符分割")
            else:
                self.mode_combo.setCurrentText("按长度分割")
            self.set_delimiter(config.get("delimiter", ","))
            self.length_spin.setValue(config.get("split_length", 10))
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "text_split"
