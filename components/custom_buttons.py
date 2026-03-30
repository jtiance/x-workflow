# -*- coding: utf-8 -*-
"""
自定义按钮组件模块
提供经过二次调整的通用按钮组件
"""

from qfluentwidgets import PushButton


class CheckablePushButton(PushButton):
    """
    可检查的推送按钮
    具有以下特性：
    1. 可被选择（checkable）
    2. 点击后自动失去焦点
    3. 保持文本原始大小写
    """
    
    def __init__(self, text, parent=None):
        """
        初始化可检查的推送按钮
        
        Args:
            text: 按钮文本
            parent: 父控件
        """
        super().__init__(parent=parent)
        
        # 设置文本
        self.setText(text)
        
        # 设置默认属性
        self.setCheckable(True)
        self.setChecked(False)
        
        # 连接点击信号，点击后失去焦点
        self.clicked.connect(self.clearFocus)
