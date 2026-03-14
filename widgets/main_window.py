# -*- coding: utf-8 -*-
"""
主窗口模块
应用程序的主窗口，包含标签页和菜单栏等
"""

from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QMenuBar, QMenu
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from widgets.tab_widget import TabContent
from widgets.control_dialog import ControlDialog
from workflow_manager import get_workflow_manager


class MainWindow(QMainWindow):
    """
    应用程序主窗口
    """
    
    def __init__(self):
        """
        初始化主窗口
        """
        super().__init__()
        
        # 初始化流程管理器
        self.workflow_manager = get_workflow_manager()
        
        # 设置窗口属性
        self.setWindowTitle("X-Workflow")
        self.setMinimumSize(1000, 700)  # 设置最小尺寸
        self.setObjectName("MainWindow")
        
        # 初始化 UI
        self._init_ui()
        
        # 创建初始标签页
        self._create_initial_tabs()
        
        # 最大化窗口
        self.showMaximized()
        
    def _init_ui(self):
        """
        初始化用户界面
        """
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建中心布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # ============= 创建标签页控件 =============
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)  # 标签可关闭
        self.tab_widget.setMovable(True)  # 标签可拖动
        self.tab_widget.setDocumentMode(True)  # 文档模式
        self.tab_widget.setObjectName("MainTabWidget")
        
        # 设置标签栏样式，只影响标签头部，不影响子控件
        self.tab_widget.tabBar().setStyleSheet("""
            QTabBar::tab {
                background: #2b2b2b;
                border: 1px solid #3c3f41;
                border-bottom: none;
                padding: 4px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #3c3f41;
                border-bottom: 1px solid #3c3f41;
            }
            QTabBar::tab:hover {
                background: #36393b;
            }
        """)
        
        # 连接标签页关闭信号
        self.tab_widget.tabCloseRequested.connect(self._on_tab_close_requested)
        
        # 将标签页添加到布局
        layout.addWidget(self.tab_widget)
        
        # ============= 创建菜单栏 =============
        self._create_menu_bar()
        
    def _create_menu_bar(self):
        """
        创建菜单栏
        """
        # 获取菜单栏
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")
        
        # 新建标签页动作
        new_tab_action = QAction("新建标签页(&N)", self)
        new_tab_action.setShortcut("Ctrl+T")
        new_tab_action.triggered.connect(self._add_new_tab)
        file_menu.addAction(new_tab_action)
        
        # 关闭标签页动作
        close_tab_action = QAction("关闭标签页(&C)", self)
        close_tab_action.setShortcut("Ctrl+W")
        close_tab_action.triggered.connect(self._close_current_tab)
        file_menu.addAction(close_tab_action)
        
        # 添加分隔符
        file_menu.addSeparator()
        
        # 退出动作
        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 查看菜单
        view_menu = menubar.addMenu("查看(&V)")
        
        # 字体子菜单
        font_menu = QMenu("字体(&F)", self)
        view_menu.addMenu(font_menu)
        
        # 放大字号动作
        zoom_in_action = QAction("放大文本字号(&I)", self)
        zoom_in_action.setShortcut("Ctrl+=")
        zoom_in_action.triggered.connect(self._zoom_in_text)
        font_menu.addAction(zoom_in_action)
        
        # 缩小字号动作
        zoom_out_action = QAction("缩小文本字号(&O)", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(self._zoom_out_text)
        font_menu.addAction(zoom_out_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")
        
        # 关于动作
        about_action = QAction("关于(&A)", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
    def _create_initial_tabs(self):
        """
        创建初始标签页
        """
        # 添加第一个标签页
        self._add_new_tab()
        
    def _add_new_tab(self, workflow_name=None):
        """
        添加一个新的标签页
        
        Args:
            workflow_name: 流程名称，如果提供则加载该流程
        """
        # 创建标签页内容
        tab_content = TabContent()
        
        # 连接添加控件请求信号
        control_panel = tab_content.get_control_panel()
        control_panel.add_control_requested.connect(
            lambda: self._on_add_control_requested(tab_content)
        )
        
        # 连接更新标签标题请求信号
        tab_content.update_tab_title_requested.connect(
            lambda title: self._on_update_tab_title_requested(tab_content, title)
        )
        
        # 连接在新标签页加载流程请求信号
        tab_content.load_workflow_in_new_tab_requested.connect(
            self._on_load_workflow_in_new_tab_requested
        )
        
        # 标签页标题
        if workflow_name:
            tab_title = workflow_name
        else:
            tab_title = "[未命名]"
        
        # 设置 TabContent 的初始名称
        tab_content.set_current_tab_name(tab_title)
        
        # 如果提供了流程名称，则加载该流程
        if workflow_name:
            self._load_workflow_to_tab(tab_content, workflow_name)
        
        # 添加到标签页控件
        self.tab_widget.addTab(tab_content, tab_title)
        
        # 切换到新标签页
        self.tab_widget.setCurrentWidget(tab_content)
        
    def _load_workflow_to_tab(self, tab_content, workflow_name):
        """
        加载流程到指定的标签页
        
        Args:
            tab_content: 标签页内容
            workflow_name: 流程名称
        """
        try:
            # 获取流程管理器
            workflow_manager = get_workflow_manager()
            
            # 加载流程配置
            controls_config = workflow_manager.load_workflow(workflow_name)
            
            if controls_config is not None:
                # 加载控件配置
                tab_content.get_control_panel().load_controls_config(controls_config)
                tab_content.set_status(f"已加载流程: {workflow_name}", is_error=False)
            else:
                tab_content.set_status(f"加载失败: 流程 '{workflow_name}' 不存在", is_error=True)
                
        except Exception as e:
            tab_content.set_status(f"加载失败: {str(e)}", is_error=True)
            
    def _on_load_workflow_in_new_tab_requested(self, workflow_name):
        """
        当请求在新标签页加载流程时调用
        
        Args:
            workflow_name: 流程名称
        """
        self._add_new_tab(workflow_name)
        
    def _on_update_tab_title_requested(self, tab_content, title):
        """
        当请求更新标签页标题时调用
        
        Args:
            tab_content: 标签页内容
            title: 新的标题
        """
        # 找到标签页的索引
        index = self.tab_widget.indexOf(tab_content)
        if index >= 0:
            self.tab_widget.setTabText(index, title)
            # 同时更新 TabContent 的内部属性
            tab_content.set_current_tab_name(title)
            
    def update_current_tab_title(self, title):
        """
        更新当前标签页的标题
        
        Args:
            title: 新的标题
        """
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            self.tab_widget.setTabText(current_index, title)
        
    def _close_current_tab(self):
        """
        关闭当前标签页
        """
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            self._on_tab_close_requested(current_index)
            
    def _on_tab_close_requested(self, index):
        """
        当请求关闭标签页时调用
        
        Args:
            index: 要关闭的标签页索引
        """
        # 至少保留一个标签页
        if self.tab_widget.count() > 1:
            # 获取标签页内容
            tab_content = self.tab_widget.widget(index)
            # 移除标签页
            self.tab_widget.removeTab(index)
            # 销毁标签页内容
            tab_content.deleteLater()
            
    def _on_add_control_requested(self, tab_content):
        """
        当请求添加控件时调用
        
        Args:
            tab_content: 要添加控件的标签页内容
        """
        # 创建控件选择对话框
        dialog = ControlDialog(self)
        
        # 连接控件选择信号
        def on_control_selected(control_type):
            self._on_control_selected(tab_content, control_type)
        
        dialog.control_selected.connect(on_control_selected)
        
        # 显示对话框
        dialog.exec()
        
    def _on_control_selected(self, tab_content, control_type):
        """
        当选择控件后调用
        
        Args:
            tab_content: 要添加控件的标签页内容
            control_type: 选中的控件类型
        """
        if control_type == "text_replace":
            # 创建文本替换控件
            from controls.text_replace import TextReplaceControl
            control = TextReplaceControl()
            # 添加到标签页
            tab_content.add_control(control)
            
        elif control_type == "json_format":
            # 创建JSON格式化控件
            from controls.json_format import JsonFormatControl
            control = JsonFormatControl()
            # 添加到标签页
            tab_content.add_control(control)
            
        elif control_type == "json_compress":
            # 创建JSON压缩控件
            from controls.json_compress import JsonCompressControl
            control = JsonCompressControl()
            # 添加到标签页
            tab_content.add_control(control)
            
        elif control_type == "add_text":
            # 创建增加文本控件
            from controls.add_text import AddTextControl
            control = AddTextControl()
            # 添加到标签页
            tab_content.add_control(control)
            
        elif control_type == "case_convert":
            # 创建大小写转换控件
            from controls.case_convert import CaseConvertControl
            control = CaseConvertControl()
            # 添加到标签页
            tab_content.add_control(control)
            
        elif control_type == "text_split":
            # 创建文本分割控件
            from controls.text_split import TextSplitControl
            control = TextSplitControl()
            # 添加到标签页
            tab_content.add_control(control)
            
        elif control_type == "text_merge":
            # 创建文本合并控件
            from controls.text_merge import TextMergeControl
            control = TextMergeControl()
            # 添加到标签页
            tab_content.add_control(control)
            
        elif control_type == "text_search_delete":
            # 创建文本搜索删除控件
            from controls.text_search_delete import TextSearchDeleteControl
            control = TextSearchDeleteControl()
            # 添加到标签页
            tab_content.add_control(control)
            
        elif control_type == "remove_duplicate":
            from controls.remove_duplicate import RemoveDuplicateControl
            control = RemoveDuplicateControl()
            tab_content.add_control(control)
            
    def _show_about(self):
        """
        显示关于对话框
        """
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            "关于 X-Workflow",
            "X-Workflow\n\n"
            "一个可视化的文本处理工作流工具\n"
            "基于 PySide6和qt-material 开发"
        )
    
    def _zoom_in_text(self):
        """
        放大当前标签页的文本字号
        """
        # 获取当前标签页
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            tab_content = self.tab_widget.widget(current_index)
            if tab_content:
                text_editor = tab_content.get_text_editor()
                if text_editor:
                    text_editor.zoom_in()
    
    def _zoom_out_text(self):
        """
        缩小当前标签页的文本字号
        """
        # 获取当前标签页
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            tab_content = self.tab_widget.widget(current_index)
            if tab_content:
                text_editor = tab_content.get_text_editor()
                if text_editor:
                    text_editor.zoom_out()
