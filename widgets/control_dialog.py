# -*- coding: utf-8 -*-
"""
控件选择对话框模块
用于选择要添加的控件类型
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
    QListWidgetItem, QLabel, QPushButton, QFrame, QSplitter, QWidget
)
from PySide6.QtCore import Qt, Signal


class ControlDialog(QDialog):
    """
    控件选择对话框
    左侧显示可用控件列表，右侧显示选中控件的预览
    """
    
    # 定义信号：当用户确认选择控件时发出
    control_selected = Signal(str)  # 控件类型名称
    
    def __init__(self, parent=None):
        """
        初始化控件选择对话框
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        
        # 设置对话框属性
        self.setWindowTitle("选择控件")
        self.setMinimumSize(600, 400)  # 设置最小尺寸
        self.setObjectName("ControlDialog")
        
        # 保存选中的控件类型
        self.selected_control = None
        
        # 初始化 UI
        self._init_ui()
        
        # 填充控件列表
        self._populate_control_list()
        
        # 清除默认选择（不选中任何项）
        self.control_list.clearSelection()
        
    def _init_ui(self):
        """
        初始化用户界面
        """
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 创建分割器，左右分隔
        splitter = QSplitter(Qt.Horizontal)
        
        # ============= 左侧：控件列表 =============
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # 列表标题
        left_title = QLabel("可用控件")
        left_title.setObjectName("ListTitle")
        
        # 控件列表
        self.control_list = QListWidget()
        self.control_list.setObjectName("ControlList")
        self.control_list.currentItemChanged.connect(self._on_selection_changed)
        self.control_list.itemDoubleClicked.connect(self._on_item_double_clicked)
        
        # 添加到左侧布局
        left_layout.addWidget(left_title)
        left_layout.addWidget(self.control_list)
        
        # ============= 右侧：预览区域 =============
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # 预览标题
        right_title = QLabel("控件预览")
        right_title.setObjectName("PreviewTitle")
        
        # 预览区域（使用 QFrame 作为容器）
        self.preview_area = QFrame()
        self.preview_area.setFrameShape(QFrame.StyledPanel)
        self.preview_area.setObjectName("PreviewArea")
        
        # 预览区域的布局
        self.preview_layout = QVBoxLayout(self.preview_area)
        self.preview_layout.setContentsMargins(10, 10, 10, 10)
        
        # 初始提示标签
        self.preview_hint = QLabel("请从左侧选择一个控件")
        self.preview_hint.setAlignment(Qt.AlignCenter)
        self.preview_layout.addWidget(self.preview_hint)
        
        # 添加到右侧布局
        right_layout.addWidget(right_title)
        right_layout.addWidget(self.preview_area)
        
        # 将左右两侧添加到分割器
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)  # 左侧占1份
        splitter.setStretchFactor(1, 2)  # 右侧占2份
        
        # ============= 底部：按钮区域 =============
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # 添加弹性空间
        
        # 确定按钮
        self.ok_button = QPushButton("确定")
        self.ok_button.setObjectName("OkButton")
        self.ok_button.clicked.connect(self._on_ok_clicked)
        self.ok_button.setEnabled(False)  # 初始禁用，直到选择控件
        
        # 取消按钮
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setObjectName("CancelButton")
        self.cancel_button.clicked.connect(self.reject)
        
        # 添加按钮
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        # 将所有部分添加到主布局
        main_layout.addWidget(splitter)
        main_layout.addLayout(button_layout)
        
    def _populate_control_list(self):
        """
        填充控件列表
        添加可用的控件类型
        """
        # 这里定义可用的控件类型
        # 格式：(显示名称, 控件类型标识)
        controls = [
            ("文本替换", "text_replace"),
            ("JSON格式化", "json_format"),
            ("增加文本", "add_text"),
            ("大小写转换", "case_convert"),
            ("文本分割", "text_split"),
            ("文本合并", "text_merge"),
            ("文本搜索删除", "text_search_delete"),
        ]
        
        # 添加到列表
        for display_name, control_type in controls:
            item = QListWidgetItem(display_name)
            item.setData(Qt.UserRole, control_type)  # 保存控件类型到 item 的数据中
            self.control_list.addItem(item)
            
    def _on_selection_changed(self, current, previous):
        """
        当列表选择改变时调用
        
        Args:
            current: 当前选中的 item
            previous: 之前选中的 item
        """
        # 清空预览区域
        self._clear_preview()
        
        if current is not None:
            # 获取选中的控件类型
            control_type = current.data(Qt.UserRole)
            self.selected_control = control_type
            
            # 启用确定按钮
            self.ok_button.setEnabled(True)
            
            # 更新预览
            self._update_preview(control_type)
        else:
            # 没有选中任何项
            self.selected_control = None
            self.ok_button.setEnabled(False)
            
            # 显示提示
            self.preview_hint = QLabel("请从左侧选择一个控件")
            self.preview_hint.setAlignment(Qt.AlignCenter)
            self.preview_layout.addWidget(self.preview_hint)
            
    def _clear_preview(self):
        """
        清空预览区域
        """
        # 移除预览布局中的所有组件
        while self.preview_layout.count():
            item = self.preview_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
    def _update_preview(self, control_type):
        """
        更新预览区域，显示选中控件的预览
        
        Args:
            control_type: 控件类型标识
        """
        if control_type == "text_replace":
            # 文本替换控件预览
            from controls.text_replace import TextReplaceControl
            
            # 创建预览控件（禁用交互，只用于显示）
            preview_control = TextReplaceControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)
            
            # 设置一些示例数据
            preview_control.set_find_text("hello")
            preview_control.set_replace_text("world")
            
            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()
            
        elif control_type == "json_format":
            # JSON格式化控件预览
            from controls.json_format import JsonFormatControl
            
            # 创建预览控件（禁用交互，只用于显示）
            preview_control = JsonFormatControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)
            
            # 设置一些示例数据
            preview_control.set_indent(4)
            preview_control.set_sort_keys(True)
            
            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()
            
        elif control_type == "add_text":
            # 增加文本控件预览
            from controls.add_text import AddTextControl
            
            # 创建预览控件（禁用交互，只用于显示）
            preview_control = AddTextControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)
            
            # 设置一些示例数据
            preview_control.set_operation_type("增加前缀")
            preview_control.set_text("> ")
            
            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()
            
        elif control_type == "case_convert":
            # 大小写转换控件预览
            from controls.case_convert import CaseConvertControl
            
            # 创建预览控件（禁用交互，只用于显示）
            preview_control = CaseConvertControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)
            
            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()
            
        elif control_type == "text_split":
            # 文本分割控件预览
            from controls.text_split import TextSplitControl
            
            # 创建预览控件（禁用交互，只用于显示）
            preview_control = TextSplitControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)
            
            # 设置一些示例数据
            preview_control.set_delimiter(",")
            
            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()
            
        elif control_type == "text_merge":
            # 文本合并控件预览
            from controls.text_merge import TextMergeControl
            
            # 创建预览控件（禁用交互，只用于显示）
            preview_control = TextMergeControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)
            
            # 设置一些示例数据
            preview_control.set_separator(", ")
            
            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()
            
        elif control_type == "text_search_delete":
            # 文本搜索删除控件预览
            from controls.text_search_delete import TextSearchDeleteControl
            
            # 创建预览控件（禁用交互，只用于显示）
            preview_control = TextSearchDeleteControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)
            
            # 设置一些示例数据
            preview_control.set_search_text("test")
            
            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()
            
    def _on_ok_clicked(self):
        """
        当点击确定按钮时调用
        """
        if self.selected_control:
            # 发出信号
            self.control_selected.emit(self.selected_control)
            # 关闭对话框，返回 Accepted
            self.accept()
            
    def _on_item_double_clicked(self, item):
        """
        当双击列表项时调用
        """
        if item:
            # 获取选中的控件类型
            self.selected_control = item.data(Qt.UserRole)
            # 发出信号
            self.control_selected.emit(self.selected_control)
            # 关闭对话框，返回 Accepted
            self.accept()
            
    def get_selected_control(self):
        """
        获取选中的控件类型
        
        Returns:
            str: 控件类型标识，如果没有选中则返回 None
        """
        return self.selected_control
