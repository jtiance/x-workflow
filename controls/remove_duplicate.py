# -*- coding: utf-8 -*-
"""
移除重复行控件模块
提供移除文本中重复行的功能
"""

from PySide6.QtWidgets import (QGridLayout, QLabel, QComboBox, QCheckBox, QSizePolicy)
from PySide6.QtCore import Qt

from controls.base_control import BaseControl


class RemoveDuplicateControl(BaseControl):
    """
    移除重复行控件类
    提供按不同方式移除重复行的功能
    """
    
    def __init__(self, parent=None):
        """
        初始化移除重复行控件
        
        Args:
            parent: 父控件
        """
        super().__init__("移除重复行", parent)
        
    def _init_content(self):
        """
        初始化内容区域
        添加移除重复行相关的控件
        """
        layout = self.get_content_layout()
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        mode_label = QLabel("模式:")
        mode_label.setMinimumWidth(70)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["保留首次出现", "保留最后一次出现"])
        self.mode_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.mode_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(mode_label, 0, 0)
        grid_layout.addWidget(self.mode_combo, 0, 1)
        
        ignore_case_label = QLabel("忽略大小写:")
        ignore_case_label.setMinimumWidth(70)
        
        self.ignore_case_check = QCheckBox()
        self.ignore_case_check.stateChanged.connect(self._emit_parameters_changed)
        self.ignore_case_check.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        grid_layout.addWidget(ignore_case_label, 1, 0)
        grid_layout.addWidget(self.ignore_case_check, 1, 1)
        
        ignore_blank_label = QLabel("忽略空行:")
        ignore_blank_label.setMinimumWidth(70)
        
        self.ignore_blank_check = QCheckBox()
        self.ignore_blank_check.stateChanged.connect(self._emit_parameters_changed)
        self.ignore_blank_check.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        grid_layout.addWidget(ignore_blank_label, 2, 0)
        grid_layout.addWidget(self.ignore_blank_check, 2, 1)
        
        grid_layout.setColumnStretch(1, 1)
        
        layout.addLayout(grid_layout)
    
    def get_mode(self):
        """
        获取当前模式
        
        Returns:
            str: 'first' 或 'last'
        """
        if self.mode_combo.currentText() == "保留首次出现":
            return "first"
        else:
            return "last"
    
    def is_ignore_case(self):
        """
        获取是否忽略大小写
        
        Returns:
            bool: 是否忽略大小写
        """
        return self.ignore_case_check.isChecked()
    
    def is_ignore_blank(self):
        """
        获取是否忽略空行
        
        Returns:
            bool: 是否忽略空行
        """
        return self.ignore_blank_check.isChecked()
    
    def execute(self, text):
        """
        执行移除重复行操作
        
        Args:
            text: 要处理的文本
            
        Returns:
            str: 处理后的文本
        """
        if not text:
            return text
        
        lines = text.split('\n')
        
        ignore_case = self.is_ignore_case()
        ignore_blank = self.is_ignore_blank()
        mode = self.get_mode()
        
        if mode == "first":
            seen = []
            result = []
            for line in lines:
                if ignore_blank and not line.strip():
                    result.append(line)
                    continue
                
                check_line = line if not ignore_case else line.lower()
                
                if check_line not in seen:
                    seen.append(check_line)
                    result.append(line)
            
            return '\n'.join(result)
        
        else:
            seen_last = {}
            for line in lines:
                if ignore_blank and not line.strip():
                    continue
                
                check_line = line if not ignore_case else line.lower()
                seen_last[check_line] = line
            
            return '\n'.join(list(seen_last.values()))
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.mode_combo.setCurrentText("保留首次出现")
        self.ignore_case_check.setChecked(False)
        self.ignore_blank_check.setChecked(False)
        
    def get_config(self):
        """
        获取控件配置
        
        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "remove_duplicate",
            "mode": self.get_mode(),
            "ignore_case": self.is_ignore_case(),
            "ignore_blank": self.is_ignore_blank()
        }
        
    def load_config(self, config):
        """
        加载控件配置
        
        Args:
            config: 控件配置字典
        """
        if config.get("type") == "remove_duplicate":
            mode = config.get("mode", "first")
            if mode == "first":
                self.mode_combo.setCurrentText("保留首次出现")
            else:
                self.mode_combo.setCurrentText("保留最后一次出现")
            self.ignore_case_check.setChecked(config.get("ignore_case", False))
            self.ignore_blank_check.setChecked(config.get("ignore_blank", False))
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "remove_duplicate"
