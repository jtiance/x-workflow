# -*- coding: utf-8 -*-
"""
主窗口模块
应用程序的主窗口，使用 FluentWindow 提供 Fluent Design 效果
"""

from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QMessageBox, QHBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import FluentWindow, NavigationItemPosition, FluentIcon as FIF, PushButton

from widgets.tab_widget import TabContent
from widgets.control_dialog import ControlDialog
from workflow_manager import get_workflow_manager


class WorkspaceInterface(QWidget):
    """
    工作区页面 - 包含标签页和编辑功能
    """
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("WorkspaceInterface")
        
        self.workflow_manager = get_workflow_manager()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # ============= 创建标签页控件 =============
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.setUsesScrollButtons(True)
        self.tab_widget.setObjectName("MainTabWidget")
        
        # 在标签页右上角添加"+"按钮
        self.new_tab_button = PushButton("+")
        self.new_tab_button.setFixedWidth(32)
        self.new_tab_button.setFixedHeight(32)
        self.new_tab_button.clicked.connect(self._add_new_tab)
        self.tab_widget.setCornerWidget(self.new_tab_button, Qt.TopRightCorner)
        
        # 连接标签页关闭信号
        self.tab_widget.tabCloseRequested.connect(self._on_tab_close_requested)
        
        # 将标签页添加到布局
        layout.addWidget(self.tab_widget)
        
        # 创建初始标签页
        self._create_initial_tabs()
        
    def _create_initial_tabs(self):
        """创建初始标签页"""
        self._add_new_tab()
        
    def _add_new_tab(self, workflow_name=None):
        """添加新标签页"""
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
            tab_title = "未命名"
        
        tab_content.set_current_tab_name(tab_title)
        
        if workflow_name:
            self._load_workflow_to_tab(tab_content, workflow_name)
        
        self.tab_widget.addTab(tab_content, tab_title)
        self.tab_widget.setCurrentWidget(tab_content)
        
    def _load_workflow_to_tab(self, tab_content, workflow_name):
        """加载流程到标签页"""
        try:
            controls_config = self.workflow_manager.load_workflow(workflow_name)
            if controls_config is not None:
                tab_content.get_control_panel().load_controls_config(controls_config)
                tab_content.set_status(f"已加载流程: {workflow_name}", is_error=False)
            else:
                tab_content.set_status(f"加载失败: 流程 '{workflow_name}' 不存在", is_error=True)
        except Exception as e:
            tab_content.set_status(f"加载失败: {str(e)}", is_error=True)
            
    def _on_load_workflow_in_new_tab_requested(self, workflow_name):
        """在新标签页加载流程"""
        self._add_new_tab(workflow_name)
        
    def _on_update_tab_title_requested(self, tab_content, title):
        """更新标签标题"""
        index = self.tab_widget.indexOf(tab_content)
        if index >= 0:
            self.tab_widget.setTabText(index, title)
            tab_content.set_current_tab_name(title)
            
    def _on_tab_close_requested(self, index):
        """关闭标签页"""
        if self.tab_widget.count() > 1:
            tab_content = self.tab_widget.widget(index)
            self.tab_widget.removeTab(index)
            tab_content.deleteLater()
            
    def _on_add_control_requested(self, tab_content):
        """添加控件请求"""
        dialog = ControlDialog(self)
        
        def on_control_selected(control_type):
            self._on_control_selected(tab_content, control_type)
        
        dialog.control_selected.connect(on_control_selected)
        dialog.exec()
        
    def _on_control_selected(self, tab_content, control_type):
        """控件选择处理"""
        if control_type == "text_replace":
            from controls.text_replace import TextReplaceControl
            control = TextReplaceControl()
            tab_content.add_control(control)
        elif control_type == "json_format":
            from controls.json_format import JsonFormatControl
            control = JsonFormatControl()
            tab_content.add_control(control)
        elif control_type == "json_compress":
            from controls.json_compress import JsonCompressControl
            control = JsonCompressControl()
            tab_content.add_control(control)
        elif control_type == "add_text":
            from controls.add_text import AddTextControl
            control = AddTextControl()
            tab_content.add_control(control)
        elif control_type == "case_convert":
            from controls.case_convert import CaseConvertControl
            control = CaseConvertControl()
            tab_content.add_control(control)
        elif control_type == "text_split":
            from controls.text_split import TextSplitControl
            control = TextSplitControl()
            tab_content.add_control(control)
        elif control_type == "text_merge":
            from controls.text_merge import TextMergeControl
            control = TextMergeControl()
            tab_content.add_control(control)
        elif control_type == "text_search_delete":
            from controls.text_search_delete import TextSearchDeleteControl
            control = TextSearchDeleteControl()
            tab_content.add_control(control)
        elif control_type == "remove_duplicate":
            from controls.remove_duplicate import RemoveDuplicateControl
            control = RemoveDuplicateControl()
            tab_content.add_control(control)
        elif control_type == "remove_empty_lines":
            from controls.remove_empty_lines import RemoveEmptyLinesControl
            control = RemoveEmptyLinesControl()
            tab_content.add_control(control)
        elif control_type == "text_trim":
            from controls.text_trim import TextTrimControl
            control = TextTrimControl()
            tab_content.add_control(control)


class MainWindow(FluentWindow):
    """
    应用程序主窗口 - 使用 FluentWindow
    """
    
    def __init__(self):
        super().__init__()
        
        # 初始化流程管理器
        self.workflow_manager = get_workflow_manager()
        
        # 设置窗口属性
        self.setWindowTitle("X-Workflow")
        self.setMinimumSize(1000, 700)
        
        # 设置窗口图标
        import sys
        from pathlib import Path
        from PySide6.QtGui import QIcon
        import platform
        
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).parent.parent
        
        if platform.system() == 'Darwin':
            icon_path = base_path / "X-Workflow.icns"
        else:
            icon_path = base_path / "X-Workflow.png"
        
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # 初始化导航
        self.initNavigation()
        
        # 最大化窗口
        self.showMaximized()
        
    def initNavigation(self):
        """初始化导航栏"""
        # 创建工作区页面
        self.workspaceInterface = WorkspaceInterface(self)
        
        # 添加导航项
        self.addSubInterface(
            self.workspaceInterface,
            FIF.HOME,
            "工作区",
            NavigationItemPosition.TOP
        )
