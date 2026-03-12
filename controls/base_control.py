# -*- coding: utf-8 -*-
"""
基础控件模块
所有流程控件的基类，提供通用功能
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QSizePolicy, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal, Qt, QMimeData
from PySide6.QtGui import QDrag


class BaseControl(QWidget):
    """
    基础控件类
    所有流程控件的基类，提供统一的容器和样式
    """
    
    # 定义信号：当参数改变时发出
    parameters_changed = Signal()
    # 定义信号：当拖拽开始时发出
    drag_started = Signal(object)
    # 定义信号：当禁用按钮被点击时发出
    disable_requested = Signal(object)
    # 定义信号：当删除按钮被点击时发出
    delete_requested = Signal(object)
    
    def __init__(self, title, parent=None):
        """
        初始化基础控件
        
        Args:
            title: 控件标题（显示在分组框上）
            parent: 父控件
        """
        super().__init__(parent)
        
        # 设置控件的对象名称
        self.setObjectName(f"{self.__class__.__name__}")
        
        # 保存标题
        self._title = title
        
        # 禁用状态
        self._is_disabled = False
        
        # 拖拽相关
        self.drag_start_pos = None
        
        # 初始化 UI
        self._init_ui()
        
    def _init_ui(self):
        """
        初始化用户界面
        创建基础的容器结构
        """
        # 设置尺寸策略，确保控件适应宽度
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumWidth(200)  # 设置合理的最小宽度
        
        # 创建主布局（垂直布局）
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 创建分组框，提供统一的视觉样式
        self.group_box = QGroupBox()
        self.group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.group_box.setMinimumWidth(200)
        # 使用样式表调整标题上边距，同时保持边框
        self.group_box.setStyleSheet("""
            QGroupBox {
                margin-top: 0px;
                padding-top: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                top: 0px;
            }
        """)
        
        # 创建分组框的主布局
        group_main_layout = QVBoxLayout(self.group_box)
        group_main_layout.setContentsMargins(10, 3, 10, 10)
        group_main_layout.setSpacing(5)
        
        # 创建标题栏布局（包含标题和操作按钮）
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 5, 0, 5)
        title_layout.setSpacing(5)
        
        # 创建标题标签
        self.title_label = QLabel(self._title)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        # 创建操作按钮容器
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)
        
        # 创建禁用按钮
        self.disable_button = QPushButton("🔒")
        self.disable_button.setToolTip("禁用控件")
        self.disable_button.setFixedSize(24, 24)
        self.disable_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                font-size: 14px;
                padding: 0px;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 0.1);
                border-radius: 3px;
            }
        """)
        self.disable_button.clicked.connect(self._on_disable_clicked)
        
        # 创建删除按钮
        self.delete_button = QPushButton("🗑️")
        self.delete_button.setToolTip("删除控件")
        self.delete_button.setFixedSize(24, 24)
        self.delete_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                font-size: 14px;
                padding: 0px;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 0.1);
                border-radius: 3px;
            }
        """)
        self.delete_button.clicked.connect(self._on_delete_clicked)
        
        button_layout.addWidget(self.disable_button)
        button_layout.addWidget(self.delete_button)
        
        title_layout.addWidget(self.title_label, 1)
        title_layout.addWidget(button_container)
        
        # 子类将在这个布局中添加自己的控件
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(8)
        
        # 将标题栏和内容布局添加到分组框主布局
        group_main_layout.addLayout(title_layout)
        group_main_layout.addLayout(self.content_layout)
        
        # 调用子类的初始化方法
        self._init_content()
        
        # 将分组框添加到主布局
        self.main_layout.addWidget(self.group_box)
        
    def _init_content(self):
        """
        初始化内容区域
        子类需要重写此方法来添加自己的控件
        
        Returns:
            QVBoxLayout: 内容布局，子类可以在此添加控件
        """
        pass
        
    def get_content_layout(self):
        """
        获取内容布局
        
        Returns:
            QVBoxLayout: 内容布局
        """
        return self.content_layout
        
    def set_title(self, title):
        """
        设置标题
        
        Args:
            title: 新标题
        """
        self._title = title
        self.title_label.setText(title)
        
    def get_title(self):
        """
        获取标题
        
        Returns:
            str: 标题
        """
        return self._title
        
    def _emit_parameters_changed(self):
        """
        触发参数改变信号
        子类在参数改变时调用此方法
        """
        self.parameters_changed.emit()
        
    def execute(self, text):
        """
        执行控件操作
        子类必须重写此方法
        
        Args:
            text: 输入文本
            
        Returns:
            str: 处理后的文本
        """
        raise NotImplementedError("子类必须实现 execute 方法")
        
    def reset_parameters(self):
        """
        重置参数到默认值
        子类可以重写此方法
        """
        pass
        
    def get_config(self):
        """
        获取控件配置
        
        Returns:
            dict: 控件配置字典
        """
        raise NotImplementedError("子类必须实现 get_config 方法")
        
    def load_config(self, config):
        """
        加载控件配置
        
        Args:
            config: 控件配置字典
        """
        raise NotImplementedError("子类必须实现 load_config 方法")
        
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        raise NotImplementedError("子类必须实现 get_control_type 方法")
    
    def is_disabled(self):
        """
        获取禁用状态
        
        Returns:
            bool: 是否被禁用
        """
        return self._is_disabled
    
    def set_disabled_state(self, disabled):
        """
        设置禁用状态
        
        Args:
            disabled: 是否禁用
        """
        self._is_disabled = disabled
        # 更新按钮图标
        if disabled:
            self.disable_button.setText("🔓")
            self.disable_button.setToolTip("启用控件")
            # 设置禁用样式并禁用所有子组件
            self.setStyleSheet("QWidget { opacity: 0.5; }")
            self._set_children_enabled(self.content_layout, False)
        else:
            self.disable_button.setText("🔒")
            self.disable_button.setToolTip("禁用控件")
            # 恢复正常样式并启用所有子组件
            self.setStyleSheet("")
            self._set_children_enabled(self.content_layout, True)
    
    def _set_child_widgets_transparent(self, parent):
        """
        递归设置子组件对鼠标事件透明（除了操作按钮）
        
        Args:
            parent: 父组件
        """
        if not parent:
            return
        
        # 遍历所有子组件
        for child in parent.findChildren(QWidget):
            # 不要让操作按钮透明（禁用和删除按钮）
            if child == self.disable_button or child == self.delete_button:
                continue
            
            # 设置对鼠标事件透明
            child.setAttribute(Qt.WA_TransparentForMouseEvents, True)
    
    def _set_children_enabled(self, layout, enabled):
        """
        递归设置布局中所有子组件的启用状态
        
        Args:
            layout: 要处理的布局
            enabled: 是否启用
        """
        if not layout:
            return
        
        # 遍历布局中的所有项
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if not item:
                continue
            
            # 如果是 widget
            widget = item.widget()
            if widget:
                # 不要禁用操作按钮（禁用和删除按钮）
                if widget != self.disable_button and widget != self.delete_button:
                    widget.setEnabled(enabled)
                continue
            
            # 如果是子布局，递归处理
            child_layout = item.layout()
            if child_layout:
                self._set_children_enabled(child_layout, enabled)
        
    def _on_disable_clicked(self):
        """
        处理禁用按钮点击事件
        """
        # 切换禁用状态
        self.set_disabled_state(not self._is_disabled)
        # 发出禁用请求信号
        self.disable_requested.emit(self)
        
    def _on_delete_clicked(self):
        """
        处理删除按钮点击事件
        """
        # 发出删除请求信号
        self.delete_requested.emit(self)
    
    def set_buttons_visible(self, visible):
        """
        设置操作按钮的可见性
        
        Args:
            visible: 是否可见
        """
        self.disable_button.setVisible(visible)
        self.delete_button.setVisible(visible)
        
    def mousePressEvent(self, event):
        """
        鼠标按下事件
        
        Args:
            event: 鼠标事件
        """
        # 检查是否点击了操作按钮
        child = self.childAt(event.position().toPoint())
        if child == self.disable_button or child == self.delete_button:
            # 点击了操作按钮，不处理拖拽
            super().mousePressEvent(event)
            return
        
        # 其他情况，记录拖拽起始位置
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.position().toPoint()
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """
        鼠标移动事件
        
        Args:
            event: 鼠标事件
        """
        if event.buttons() == Qt.LeftButton and self.drag_start_pos:
            # 检查是否移动了足够的距离
            distance = (event.position().toPoint() - self.drag_start_pos).manhattanLength()
            if distance >= 10:
                # 开始拖拽
                self._start_drag()
        super().mouseMoveEvent(event)
        
    def _start_drag(self):
        """
        开始拖拽
        """
        # 创建拖拽对象
        drag = QDrag(self)
        
        # 创建 mime 数据
        mime_data = QMimeData()
        mime_data.setText("拖动控件以改变顺序")  # 标识这是控件拖拽
        
        drag.setMimeData(mime_data)
        
        # 发出拖拽开始信号
        self.drag_started.emit(self)
        
        # 执行拖拽
        drag.exec(Qt.MoveAction)
