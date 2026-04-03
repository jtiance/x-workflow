# -*- coding: utf-8 -*-
"""
自定义通用对话框模块
实现类似qfluentWidgets pro版本的对话框效果，支持灵活自定义内容和按钮
"""

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QWidget
)
from qfluentwidgets import PushButton, PrimaryPushButton


class CustomDialog(QDialog):
    """
    自定义通用对话框
    支持灵活添加内容组件和底部按钮，实现圆角效果和自适应布局
    """

    def __init__(self, title="对话框", parent=None):
        """
        初始化自定义对话框

        Args:
            title: 对话框标题
            parent: 父控件
        """
        super().__init__(parent)

        # 初始化属性
        self.buttons = []  # 存储所有按钮
        self.content_layout = None  # 内容区域布局
        self.button_layout = None  # 按钮区域布局

        # 设置对话框属性
        self.setWindowTitle(title)
        self.setMinimumSize(300, 150)
        self.setObjectName("CustomDialog")

        # 初始化UI
        self.__init_ui()

        # 初始化样式
        self.__init_style()

    def __init_ui(self):
        """
        初始化用户界面（私有方法，避免子类重写）
        """
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 内容区域
        self.content_container = QWidget()
        self.content_container.setObjectName("ContentContainer")
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(15)
        main_layout.addWidget(self.content_container, 1)  # 伸展因子1，占剩余空间

        # 按钮区域
        self.button_container = QWidget()
        self.button_container.setObjectName("ButtonContainer")
        self.button_layout = QHBoxLayout(self.button_container)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(1)  # 按钮之间保留1px分隔线
        main_layout.addWidget(self.button_container)

    def __init_style(self):
        """
        初始化样式表，实现圆角效果和深色主题适配（私有方法，避免子类重写）
        """
        self.setStyleSheet("""
            /* 对话框整体样式 */
            QDialog#CustomDialog {
                background-color: #272727;
                border-radius: 12px;
                border: 1px solid #404040;
            }

            /* 内容容器样式 */
            QWidget#ContentContainer {
                background-color: #272727;
            }

            /* 按钮容器样式 */
            QWidget#ButtonContainer {
                background-color: #3a3a3a;
                border-bottom-left-radius: 12px;
                border-bottom-right-radius: 12px;
            }

            /* 按钮通用样式 */
            PushButton, PrimaryPushButton {
                height: 42px;
                border: none;
                border-radius: 0;
                font-size: 14px;
                color: #ffffff;
            }

            /* 普通按钮样式 */
            PushButton {
                background-color: #3a3a3a;
            }

            /* 第一个按钮左下角圆角 */
            PushButton:first-child, PrimaryPushButton:first-child {
                border-bottom-left-radius: 12px;
            }

            /* 最后一个按钮右下角圆角 */
            PushButton:last-child, PrimaryPushButton:last-child {
                border-bottom-right-radius: 12px;
            }

            /* 按钮悬停效果 */
            PushButton:hover {
                background-color: #454545;
            }

            PushButton:pressed {
                background-color: #505050;
            }

            /* 主按钮样式 */
            PrimaryPushButton {
                background-color: #0078d4;
                color: white;
            }

            PrimaryPushButton:hover {
                background-color: #106ebe;
            }

            PrimaryPushButton:pressed {
                background-color: #005a9e;
            }
        """)

    def add_content_widget(self, widget, stretch=0):
        """
        添加自定义组件到内容区域

        Args:
            widget: QWidget 要添加的组件
            stretch: int 伸展因子，默认为0
        """
        self.content_layout.addWidget(widget, stretch)

    def add_button(self, text, callback=None, is_primary=False, is_reject=False, is_accept=False):
        """
        添加底部按钮

        Args:
            text: str 按钮显示文本
            callback: callable 按钮点击回调函数
            is_primary: bool 是否为主按钮（PrimaryPushButton）
            is_reject: bool 点击是否调用reject()关闭对话框
            is_accept: bool 点击是否调用accept()关闭对话框

        Returns:
            PushButton/PrimaryPushButton 创建的按钮对象
        """
        # 创建按钮
        if is_primary:
            button = PrimaryPushButton(text)
        else:
            button = PushButton(text)

        # 绑定点击事件
        def _on_clicked():
            if callback:
                callback()
            if is_reject:
                self.reject()
            if is_accept:
                self.accept()

        button.clicked.connect(_on_clicked)

        # 添加到布局，平分宽度
        self.button_layout.addWidget(button, 1)  # 伸展因子1，所有按钮平分宽度
        self.buttons.append(button)

        return button

    def set_content_spacing(self, spacing):
        """
        设置内容区域组件间距

        Args:
            spacing: int 间距像素值
        """
        self.content_layout.setSpacing(spacing)

    def set_content_margins(self, left, top, right, bottom):
        """
        设置内容区域内边距

        Args:
            left: int 左边距
            top: int 上边距
            right: int 右边距
            bottom: int 下边距
        """
        self.content_layout.setContentsMargins(left, top, right, bottom)

    def get_button(self, index):
        """
        根据索引获取按钮

        Args:
            index: int 按钮索引，从0开始

        Returns:
            PushButton/PrimaryPushButton 按钮对象，如果索引无效返回None
        """
        if 0 <= index < len(self.buttons):
            return self.buttons[index]
        return None

    def clear_buttons(self):
        """
        清空所有按钮
        """
        while self.button_layout.count():
            item = self.button_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.buttons.clear()

    def clear_content(self):
        """
        清空内容区域所有组件
        """
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
