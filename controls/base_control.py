# -*- coding: utf-8 -*-
"""
基础控件模块
所有流程控件的基类，提供通用功能
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QSizePolicy
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
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        
        # 创建分组框，提供统一的视觉样式
        self.group_box = QGroupBox(self._title)
        self.group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.group_box.setMinimumWidth(200)
        
        # 子类将在这个布局中添加自己的控件
        self.content_layout = QVBoxLayout(self.group_box)
        self.content_layout.setSpacing(8)
        
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
        self.group_box.setTitle(title)
        
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
        
    def mousePressEvent(self, event):
        """
        鼠标按下事件
        
        Args:
            event: 鼠标事件
        """
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
