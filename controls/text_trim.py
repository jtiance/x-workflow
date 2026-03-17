# -*- coding: utf-8 -*-
"""
文本裁剪控件模块
提供根据匹配字符串裁剪文本的功能
"""

from PySide6.QtWidgets import (QGridLayout, QLabel, QComboBox, QLineEdit)
from PySide6.QtCore import Qt

from controls.base_control import BaseControl


class TextTrimControl(BaseControl):
    """
    文本裁剪控件类
    提供根据匹配字符串裁剪文本的功能
    """
    
    def __init__(self, parent=None):
        """
        初始化文本裁剪控件
        
        Args:
            parent: 父控件
        """
        super().__init__("文本裁剪", parent)
        
    def _init_content(self):
        """
        初始化内容区域
        添加文本裁剪相关的控件
        """
        layout = self.get_content_layout()
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # 第 1 行：匹配字符串
        match_label = QLabel("匹配字符串:")
        match_label.setMinimumWidth(70)
        match_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.match_edit = QLineEdit()
        self.match_edit.textChanged.connect(self._emit_parameters_changed)
        
        grid_layout.addWidget(match_label, 0, 0)
        grid_layout.addWidget(self.match_edit, 0, 1)
        
        # 第 2 行：裁剪方向
        direction_label = QLabel("裁剪方向:")
        direction_label.setMinimumWidth(70)
        direction_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.direction_combo = QComboBox()
        self.direction_combo.addItem("裁剪掉左侧的字符串", "before")
        self.direction_combo.addItem("裁剪掉右侧的字符串", "after")
        self.direction_combo.currentIndexChanged.connect(self._emit_parameters_changed)
        
        grid_layout.addWidget(direction_label, 1, 0)
        grid_layout.addWidget(self.direction_combo, 1, 1)
        
        # 第 3 行：是否裁剪匹配的文本
        include_label = QLabel("裁剪匹配的文本:")
        include_label.setMinimumWidth(70)
        include_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.include_combo = QComboBox()
        self.include_combo.addItem("是", False)
        self.include_combo.addItem("否", True)
        self.include_combo.currentIndexChanged.connect(self._emit_parameters_changed)
        
        grid_layout.addWidget(include_label, 2, 0)
        grid_layout.addWidget(self.include_combo, 2, 1)
        
        grid_layout.setColumnStretch(1, 1)
        
        layout.addLayout(grid_layout)
    
    def get_match_text(self):
        """
        获取匹配的字符串
        
        Returns:
            str: 匹配的字符串
        """
        return self.match_edit.text()
    
    def get_direction(self):
        """
        获取裁剪方向
        
        Returns:
            str: 裁剪方向 ('before' 或 'after')
        """
        return self.direction_combo.currentData()
    
    def get_include(self):
        """
        获取是否包含匹配的字符串
        
        Returns:
            bool: 是否包含匹配的字符串
        """
        return self.include_combo.currentData()
    
    def execute(self, text):
        """
        执行文本裁剪操作，对每一行都执行相同的操作
        
        Args:
            text: 要处理的文本
            
        Returns:
            str: 处理后的文本
        """
        if not text:
            return text
        
        match_text = self.get_match_text()
        if not match_text:
            return text
        
        lines = text.split('\n')
        result = []
        
        direction = self.get_direction()
        include = self.get_include()
        
        for line in lines:
            pos = line.find(match_text)
            if pos == -1:
                result.append(line)
                continue
            
            if direction == "before":
                if include:
                    result.append(line[pos:])
                else:
                    result.append(line[pos + len(match_text):])
            else:
                if include:
                    result.append(line[:pos + len(match_text)])
                else:
                    result.append(line[:pos])
        
        return '\n'.join(result)
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.match_edit.clear()
        self.direction_combo.setCurrentIndex(0)
        self.include_combo.setCurrentIndex(0)
        
    def get_config(self):
        """
        获取控件配置
        
        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "text_trim",
            "match_text": self.get_match_text(),
            "direction": self.get_direction(),
            "include": self.get_include()
        }
        
    def load_config(self, config):
        """
        加载控件配置
        
        Args:
            config: 控件配置字典
        """
        if config.get("type") == "text_trim":
            self.match_edit.setText(config.get("match_text", ""))
            direction = config.get("direction", "before")
            include = config.get("include", False)
            
            direction_index = self.direction_combo.findData(direction)
            if direction_index != -1:
                self.direction_combo.setCurrentIndex(direction_index)
                
            include_index = self.include_combo.findData(include)
            if include_index != -1:
                self.include_combo.setCurrentIndex(include_index)
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "text_trim"
