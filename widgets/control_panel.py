# -*- coding: utf-8 -*-
"""
控制面板模块
提供左侧的控件列表管理功能
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QPushButton, QFrame, QHBoxLayout
)
from PySide6.QtCore import Qt, Signal, QPoint


class ControlPanel(QWidget):
    """
    控制面板组件
    包含一个可滚动的区域用于显示已添加的控件，
    底部有"+"按钮用于添加新控件和EXE按钮用于执行
    """
    
    # 定义信号：当点击添加按钮时发出
    add_control_requested = Signal()
    # 定义信号：当点击执行按钮时发出
    run_requested = Signal()
    # 定义信号：当点击加载按钮时发出
    load_requested = Signal()
    # 定义信号：当点击保存按钮时发出
    save_requested = Signal()
    
    def __init__(self, parent=None):
        """
        初始化控制面板
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        
        # 设置控件的对象名称
        self.setObjectName("ControlPanel")
        
        # 保存已添加的控件列表
        self.controls = []
        
        # 拖拽相关
        self.dragging_control = None
        
        # 初始化 UI
        self._init_ui()
        
        # 设置接受拖拽
        self.setAcceptDrops(True)
        
    def _init_ui(self):
        """
        初始化用户界面
        """
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 设置大小策略，确保高度一致
        from PySide6.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # ============= 顶部：工具栏 =============
        # 创建工具栏
        toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setContentsMargins(5, 5, 5, 5)
        toolbar_layout.setSpacing(2)
        
        # 保存按钮（图标）
        self.save_button = QPushButton("💾")
        self.save_button.setToolTip("保存/更新")
        self.save_button.setMinimumSize(50, 40)
        self.save_button.setMaximumSize(50, 40)
        self.save_button.setObjectName("SaveButton")
        self.save_button.setStyleSheet("QPushButton { font-size: 20px; border: none; background: transparent; }")
        self.save_button.clicked.connect(self.save_requested.emit)
        
        # 管理流程按钮（图标）
        self.load_button = QPushButton("📋")
        self.load_button.setToolTip("流程管理器")
        self.load_button.setMinimumSize(50, 40)
        self.load_button.setMaximumSize(50, 40)
        self.load_button.setObjectName("LoadButton")
        self.load_button.setStyleSheet("QPushButton { font-size: 20px; border: none; background: transparent; }")
        self.load_button.clicked.connect(self.load_requested.emit)
        
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.save_button)
        toolbar_layout.addWidget(self.load_button)
        
        # ============= 中间：滚动区域 =============
        # 创建滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # 让内容自动调整大小
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏水平滚动条
        self.scroll_area.setObjectName("ControlScrollArea")
        
        # 创建滚动区域的内容容器
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.addStretch()  # 添加弹性空间，让控件靠上排列
        
        # 将内容容器设置到滚动区域
        self.scroll_area.setWidget(self.scroll_content)
        
        # ============= 底部：按钮区域 =============
        # 创建按钮容器
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)
        
        # 创建添加按钮
        self.add_button = QPushButton("添加")
        self.add_button.setMinimumHeight(50)  # 设置最小高度为50
        self.add_button.setMinimumWidth(60)  # 设置最小宽度，更窄
        self.add_button.setObjectName("AddControlButton")
        self.add_button.clicked.connect(self.add_control_requested.emit)
        
        # 创建执行按钮
        self.run_button = QPushButton("执行")
        self.run_button.setMinimumHeight(50)  # 设置最小高度为50
        self.run_button.setMinimumWidth(60)  # 设置最小宽度，更窄
        self.run_button.setObjectName("RunButton")
        self.run_button.clicked.connect(self.run_requested.emit)
        
        # 添加按钮到布局（左侧固定10px间距，按钮可拉伸）
        button_layout.addSpacing(10)
        button_layout.addWidget(self.add_button, 1)  # 伸展因子1
        button_layout.addWidget(self.run_button, 1)  # 伸展因子1
        
        # 将工具栏、滚动区域和按钮区域添加到主布局
        main_layout.addWidget(toolbar_widget)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(button_widget)
        
    def set_save_button_text(self, text):
        """
        设置保存按钮的文本（工具提示）
        
        Args:
            text: 按钮文本
        """
        if text == "更新":
            self.save_button.setToolTip("更新")
        else:
            self.save_button.setToolTip("保存/更新")
        
    def add_control(self, control_widget):
        """
        添加一个控件到面板
        
        Args:
            control_widget: 要添加的控件（QWidget 实例）
        """
        # 在弹性空间之前插入控件
        insert_index = self.scroll_layout.count() - 1  # 减1是因为最后一个是 stretch
        self.scroll_layout.insertWidget(insert_index, control_widget)
        
        # 连接拖拽开始信号
        control_widget.drag_started.connect(self._on_control_drag_started)
        
        # 连接禁用和删除信号
        if hasattr(control_widget, 'disable_requested'):
            control_widget.disable_requested.connect(self._on_control_disable_requested)
        if hasattr(control_widget, 'delete_requested'):
            control_widget.delete_requested.connect(self._on_control_delete_requested)
        
        # 保存到控件列表
        self.controls.append(control_widget)
        
    def remove_control(self, control_widget):
        """
        从面板中移除一个控件
        
        Args:
            control_widget: 要移除的控件
        """
        if control_widget in self.controls:
            # 从布局中移除
            self.scroll_layout.removeWidget(control_widget)
            # 从列表中移除
            self.controls.remove(control_widget)
            # 销毁控件
            control_widget.deleteLater()
            
    def clear_controls(self):
        """
        清空所有控件
        """
        # 反向遍历并移除所有控件
        for control in reversed(self.controls):
            self.remove_control(control)
            
    def get_controls(self):
        """
        获取所有已添加的控件
        
        Returns:
            list: 控件列表
        """
        return self.controls.copy()
        
    def get_controls_config(self):
        """
        获取所有控件的配置
        
        Returns:
            list: 控件配置列表
        """
        configs = []
        for control in self.controls:
            if hasattr(control, 'get_config'):
                configs.append(control.get_config())
        return configs
        
    def load_controls_config(self, configs):
        """
        加载控件配置
        
        Args:
            configs: 控件配置列表
        """
        # 清空现有控件
        self.clear_controls()
        
        # 根据配置创建控件
        from controls.text_replace import TextReplaceControl
        from controls.json_format import JsonFormatControl
        from controls.add_text import AddTextControl
        from controls.case_convert import CaseConvertControl
        from controls.text_split import TextSplitControl
        from controls.text_merge import TextMergeControl
        from controls.text_search_delete import TextSearchDeleteControl
        
        for config in configs:
            control_type = config.get("type")
            
            if control_type == "text_replace":
                control = TextReplaceControl()
                control.load_config(config)
                self.add_control(control)
            elif control_type == "json_format":
                control = JsonFormatControl()
                control.load_config(config)
                self.add_control(control)
            elif control_type == "add_text":
                control = AddTextControl()
                control.load_config(config)
                self.add_control(control)
            elif control_type == "case_convert":
                control = CaseConvertControl()
                control.load_config(config)
                self.add_control(control)
            elif control_type == "text_split":
                control = TextSplitControl()
                control.load_config(config)
                self.add_control(control)
            elif control_type == "text_merge":
                control = TextMergeControl()
                control.load_config(config)
                self.add_control(control)
            elif control_type == "text_search_delete":
                control = TextSearchDeleteControl()
                control.load_config(config)
                self.add_control(control)
    
    def _on_control_drag_started(self, control):
        """
        当控件开始拖拽时调用
        
        Args:
            control: 被拖拽的控件
        """
        self.dragging_control = control
    
    def dragEnterEvent(self, event):
        """
        拖拽进入事件
        
        Args:
            event: 拖拽事件
        """
        if event.mimeData().hasText() and event.mimeData().text() == "拖动控件以改变顺序":
            event.acceptProposedAction()
            
    def dragMoveEvent(self, event):
        """
        拖拽移动事件
        
        Args:
            event: 拖拽事件
        """
        if event.mimeData().hasText() and event.mimeData().text() == "拖动控件以改变顺序":
            event.acceptProposedAction()
            
    def dropEvent(self, event):
        """
        拖拽放下事件
        
        Args:
            event: 拖拽事件
        """
        if event.mimeData().hasText() and event.mimeData().text() == "拖动控件以改变顺序":
            # 获取拖拽位置（相对于滚动内容）
            drop_pos = event.position().toPoint()
            drop_pos = self.scroll_content.mapFromGlobal(drop_pos)
            
            # 找到插入位置
            insert_index = self._find_insert_index(drop_pos)
            
            # 重新排序控件
            self._reorder_controls(self.dragging_control, insert_index)
            
            event.acceptProposedAction()
            self.dragging_control = None
            
    def _find_insert_index(self, drop_pos):
        """
        根据拖拽位置找到插入索引
        
        Args:
            drop_pos: 放下位置（相对于滚动内容）
            
        Returns:
            int: 插入索引
        """
        # 遍历所有控件，找到应该插入的位置
        for i, control in enumerate(self.controls):
            # 获取控件的位置（相对于滚动内容）
            control_pos = control.mapTo(self.scroll_content, QPoint(0, 0))
            control_height = control.height()
            
            # 如果拖拽位置在控件的上半部分，插入到这个控件之前
            if drop_pos.y() < control_pos.y() + control_height / 2:
                return i
                
        # 如果在所有控件之后，插入到末尾
        return len(self.controls)
        
    def _reorder_controls(self, dragged_control, insert_index):
        """
        重新排序控件
        
        Args:
            dragged_control: 被拖拽的控件
            insert_index: 插入索引
        """
        # 从列表中移除被拖拽的控件
        old_index = self.controls.index(dragged_control)
        self.controls.pop(old_index)
        
        # 从布局中移除被拖拽的控件
        self.scroll_layout.removeWidget(dragged_control)
        
        # 确定新的插入位置
        if old_index < insert_index:
            insert_index -= 1  # 因为移除了一个元素，索引要减1
        
        # 插入到新位置
        self.controls.insert(insert_index, dragged_control)
        
        # 在布局中插入控件
        self.scroll_layout.insertWidget(insert_index, dragged_control)
    
    def _on_control_disable_requested(self, control):
        """
        处理控件禁用请求
        
        Args:
            control: 要禁用的控件
        """
        # 禁用状态的处理逻辑已经在控件内部实现
        # 这里可以添加额外的处理逻辑，比如更新状态栏等
        pass
    
    def _on_control_delete_requested(self, control):
        """
        处理控件删除请求
        
        Args:
            control: 要删除的控件
        """
        self.remove_control(control)
