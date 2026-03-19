# -*- coding: utf-8 -*-
"""
自定义按钮组件模块
提供经过二次调整的通用按钮组件
"""

from PySide6.QtWidgets import QPushButton


class CheckablePushButton(QPushButton):
    """
    可检查的推送按钮
    具有以下特性：
    1. 可被选择（checkable）
    2. 点击后自动失去焦点
    3. 固定内边距，确保文本不被截断
    4. 保持文本原始大小写
    5. 扁平化外观
    """
    
    def __init__(self, text, parent=None):
        """
        初始化可检查的推送按钮
        
        Args:
            text: 按钮文本
            parent: 父控件
        """
        super().__init__(text, parent)
        
        # 设置默认属性
        self.setCheckable(True)
        self.setChecked(False)
        self.setFlat(True)
        self.setStyleSheet("text-transform: none; padding: 0 4px;")
        
        # 连接点击信号，点击后失去焦点
        self.clicked.connect(self.clearFocus)
