# -*- coding: utf-8 -*-
"""
大小写转换控件模块
提供英文字母大小写转换功能
"""

from PySide6.QtWidgets import QGridLayout, QLabel, QComboBox, QSizePolicy
from PySide6.QtCore import Qt

from controls.base_control import BaseControl


class CaseConvertControl(BaseControl):
    """
    大小写转换控件类
    提供英文字母大小写转换功能
    """
    
    def __init__(self, parent=None):
        """
        初始化大小写转换控件
        
        Args:
            parent: 父控件
        """
        super().__init__("大小写转换", parent)
        
    def _init_content(self):
        """
        初始化内容区域
        添加大小写转换相关的控件
        """
        layout = self.get_content_layout()
        
        # 使用GridLayout确保对齐
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # 第1行：转换模式
        mode_label = QLabel("转换为:")
        mode_label.setMinimumWidth(70)
        mode_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "全部大写",
            "全部小写",
            "段落首字母大写",
            "每个单词首字母大写"
        ])
        self.mode_combo.setCurrentIndex(0)
        self.mode_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.mode_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(mode_label, 0, 0)
        grid_layout.addWidget(self.mode_combo, 0, 1)
        
        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)
        
        # 将GridLayout添加到内容布局
        layout.addLayout(grid_layout)
    
    def get_convert_mode(self):
        """
        获取当前转换模式
        
        Returns:
            str: 转换模式
        """
        index = self.mode_combo.currentIndex()
        modes = ["upper", "lower", "capitalize", "title"]
        return modes[index] if index < len(modes) else "upper"
    
    def set_convert_mode(self, mode):
        """
        设置转换模式
        
        Args:
            mode: 转换模式
        """
        mode_map = {
            "upper": 0,
            "lower": 1,
            "capitalize": 2,
            "title": 3
        }
        index = mode_map.get(mode, 0)
        self.mode_combo.setCurrentIndex(index)
    
    def execute(self, text):
        """
        执行大小写转换操作
        
        Args:
            text: 要处理的文本
            
        Returns:
            str: 处理后的文本
        """
        mode = self.get_convert_mode()
        
        if mode == "upper":
            return text.upper()
        elif mode == "lower":
            return text.lower()
        elif mode == "capitalize":
            return text.capitalize()
        elif mode == "title":
            return text.title()
        
        return text
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.mode_combo.setCurrentIndex(0)
        
    def get_config(self):
        """
        获取控件配置
        
        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "case_convert",
            "convert_mode": self.get_convert_mode()
        }
        
    def load_config(self, config):
        """
        加载控件配置
        
        Args:
            config: 控件配置字典
        """
        if config.get("type") == "case_convert":
            self.set_convert_mode(config.get("convert_mode", "upper"))
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "case_convert"
