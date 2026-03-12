# -*- coding: utf-8 -*-
"""
标签页组件模块
包含单个标签页的内容（左侧控制面板 + 右侧文本编辑器）
"""

import json
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSplitter, QVBoxLayout, QLabel, QFileDialog, QApplication
from PySide6.QtCore import Qt, Signal

from widgets.control_panel import ControlPanel
from widgets.text_editor import TextEditor
from widgets.workflow_dialogs import SaveWorkflowDialog, WorkflowManagerDialog
from widgets.arrow_button import ArrowButton
from workflow_manager import get_workflow_manager


class TabContent(QWidget):
    """
    标签页内容组件
    包含左侧控制面板和右侧文本编辑器
    """
    
    # 定义信号：请求更新标签标题
    update_tab_title_requested = Signal(str)
    # 定义信号：请求在新标签页加载流程
    load_workflow_in_new_tab_requested = Signal(str)
    
    def __init__(self, parent=None):
        """
        初始化标签页内容
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        
        # 设置控件的对象名称
        self.setObjectName("TabContent")
        
        # 当前标签页名称
        self._current_tab_name = "[未命名]"
        
        # 文本缓存列表（保存每个控件执行后的文本）
        self._text_cache = []
        
        # 箭头按钮列表
        self._arrow_buttons = []
        
        # 当前选中的按钮索引
        self._selected_button_index = -1
        
        # 初始化 UI
        self._init_ui()
        
        # 连接信号
        self._connect_signals()
        
        # 更新保存按钮文本
        self._update_save_button_text()
        
    def set_current_tab_name(self, name):
        """
        设置当前标签页名称
        
        Args:
            name: 标签页名称
        """
        self._current_tab_name = name
        # 更新保存按钮文本
        self._update_save_button_text()
        
    def get_current_tab_name(self):
        """
        获取当前标签页名称
        
        Returns:
            str: 标签页名称
        """
        return self._current_tab_name
        
    def _update_save_button_text(self):
        """
        根据当前标签名称更新保存按钮文本
        """
        if self._current_tab_name != "[未命名]":
            self.control_panel.set_save_button_text("更新")
        else:
            self.control_panel.set_save_button_text("保存")
        
    def _init_ui(self):
        """
        初始化用户界面
        """
        # 创建主布局（垂直布局）
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建右侧容器（包含文本编辑器和按钮列表）
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(15)  # 设置间距，让按钮区域和文本框拉开距离
        
        # 创建分割器，左右分隔
        splitter = QSplitter(Qt.Horizontal)
        splitter.setObjectName("TabSplitter")
        
        # ============= 左侧：控制面板 =============
        self.control_panel = ControlPanel()
        self.control_panel.setObjectName("TabControlPanel")
        
        # ============= 右侧：文本编辑器 =============
        self.text_editor = TextEditor()
        self.text_editor.setObjectName("TabTextEditor")
        
        # ============= 箭头按钮列表 =============
        self.button_list_widget = QWidget()
        self.button_list_widget.setMinimumHeight(60)  # 设置固定高度
        self.button_list_layout = QHBoxLayout(self.button_list_widget)
        self.button_list_layout.setContentsMargins(10, 5, 10, 0)  # 取消下边距
        self.button_list_layout.setSpacing(5)
        self.button_list_layout.setAlignment(Qt.AlignLeft)  # 靠左对齐
        
        # 将文本编辑器和按钮列表添加到右侧容器
        right_layout.addWidget(self.text_editor, 1)  # 文本编辑器占剩余空间
        right_layout.addWidget(self.button_list_widget)  # 按钮列表
        
        # 将两侧添加到分割器
        splitter.addWidget(self.control_panel)
        splitter.addWidget(right_container)
        splitter.setStretchFactor(0, 1)  # 左侧占1份（10%）
        splitter.setStretchFactor(1, 9)  # 右侧占9份（90%）
        
        # 设置初始分割位置（左侧10%，右侧90%）
        # 获取屏幕宽度
        screen = QApplication.primaryScreen()
        if screen:
            total_width = screen.availableGeometry().width()
        else:
            total_width = 1600  # 备用假设值
        splitter.setSizes([int(total_width * 0.2), int(total_width * 0.8)])
        
        # ============= 底部：状态栏 =============
        self.status_label = QLabel("就绪")
        self.status_label.setMinimumHeight(30)
        self.status_label.setObjectName("StatusLabel")
        self.status_label.setStyleSheet("padding-left: 10px; color: #aaa;")
        
        # 将分割器和状态栏添加到主布局
        main_layout.addWidget(splitter, 1)  # 分割器占剩余空间
        main_layout.addWidget(self.status_label)
        
    def _connect_signals(self):
        """
        连接各个组件的信号
        """
        # 连接执行按钮信号
        self.control_panel.run_requested.connect(self._on_execute_clicked)
        # 连接加载按钮信号
        self.control_panel.load_requested.connect(self._on_load_clicked)
        # 连接保存按钮信号
        self.control_panel.save_requested.connect(self._on_save_clicked)
        
    def _on_execute_clicked(self):
        """
        当点击 EXE 按钮时调用
        按顺序执行所有控件（跳过被禁用的控件）
        """
        try:
            # 获取当前文本（原始文本）
            original_text = self.text_editor.get_text()
            
            # 清空文本缓存
            self._text_cache = []
            # 保存原始文本作为第一个缓存
            self._text_cache.append(original_text)
            
            # 按顺序执行所有控件（跳过被禁用的）
            result_text = original_text
            for control in self.control_panel.get_controls():
                # 检查控件是否被禁用
                if hasattr(control, 'is_disabled') and control.is_disabled():
                    continue  # 跳过被禁用的控件
                
                # 检查控件是否有 execute 方法
                if hasattr(control, 'execute'):
                    result_text = control.execute(result_text)
                    # 保存每个控件执行后的文本
                    self._text_cache.append(result_text)
            
            # 更新文本编辑器（显示最终结果）
            self.text_editor.set_text(result_text)
            
            # 更新箭头按钮列表
            self._update_arrow_buttons()
            
            # 选中最新的按钮（最后一个）
            if self._arrow_buttons:
                self._select_button(len(self._arrow_buttons) - 1)
            
            # 显示成功状态
            self.set_status("执行完成", is_error=False)
            
        except json.JSONDecodeError:
            self.set_status("JSON格式化出错", is_error=True)
        except Exception as e:
            # 其他错误
            error_msg = str(e)
            self.set_status(f"执行出错: {error_msg}", is_error=True)
    
    def _update_arrow_buttons(self):
        """
        更新箭头按钮列表
        """
        # 清空现有按钮（保留布局）
        while self.button_list_layout.count():
            item = self.button_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self._arrow_buttons.clear()
        
        # 获取所有控件（不包括被禁用的）
        controls = self.control_panel.get_controls()
        enabled_controls = [c for c in controls if not (hasattr(c, 'is_disabled') and c.is_disabled())]
        
        # 创建按钮：第一个显示原始文本，后续显示每个控件的标题
        # 按钮数量 = 启用控件数量 + 1
        button_count = len(enabled_controls) + 1
        
        for i in range(button_count):
            if i == 0:
                # 第一个按钮显示原始文本
                button_text = "原始文本"
            else:
                # 后续按钮显示控件标题
                control = enabled_controls[i - 1]
                button_text = control.get_title() if hasattr(control, 'get_title') else f"步骤{i}"
            
            button = ArrowButton(button_text)
            button.setMinimumWidth(80)
            button.clicked.connect(lambda checked, index=i: self._on_arrow_button_clicked(index))
            
            self._arrow_buttons.append(button)
            self.button_list_layout.addWidget(button)
        
        # 不再添加弹性空间，确保按钮靠左对齐
    
    def _on_arrow_button_clicked(self, index):
        """
        当点击箭头按钮时调用
        
        Args:
            index: 按钮索引
        """
        # 选中新按钮
        self._select_button(index)
        
        # 显示对应索引的文本
        if 0 <= index < len(self._text_cache):
            self.text_editor.set_text(self._text_cache[index])
            self.set_status(f"显示步骤 {index} 的结果", is_error=False)
    
    def _select_button(self, index):
        """
        选中指定索引的按钮
        
        Args:
            index: 按钮索引
        """
        # 取消之前选中的按钮
        if 0 <= self._selected_button_index < len(self._arrow_buttons):
            self._arrow_buttons[self._selected_button_index].set_selected(False)
        
        # 选中新按钮
        self._selected_button_index = index
        if 0 <= index < len(self._arrow_buttons):
            self._arrow_buttons[index].set_selected(True)
            
    def _on_load_clicked(self):
        """
        当点击 MANAGE 按钮时调用
        打开流程管理器
        """
        # 获取流程管理器
        workflow_manager = get_workflow_manager()
        
        # 获取所有流程名称
        workflow_names = workflow_manager.get_workflow_names()
        
        if not workflow_names:
            self.set_status("没有可管理的流程", is_error=True)
            return
            
        # 创建流程管理器对话框
        dialog = WorkflowManagerDialog(workflow_names, self)
        
        # 连接使用信号
        def on_use_confirmed(name):
            self._on_use_workflow_confirmed(name)
        
        dialog.use_confirmed.connect(on_use_confirmed)
        
        # 连接删除信号
        def on_delete_confirmed(name):
            self._on_delete_workflow_confirmed(name)
        
        dialog.delete_confirmed.connect(on_delete_confirmed)
        
        # 连接重命名信号
        def on_rename_confirmed(old_name, new_name):
            self._on_rename_workflow_confirmed(old_name, new_name)
        
        dialog.rename_confirmed.connect(on_rename_confirmed)
        
        # 显示对话框
        dialog.exec()
        
    def _on_use_workflow_confirmed(self, name):
        """
        当确认使用流程时调用
        
        Args:
            name: 流程名称
        """
        # 发出信号，请求在新标签页加载流程
        self.load_workflow_in_new_tab_requested.emit(name)
        
    def _on_delete_workflow_confirmed(self, name):
        """
        当确认删除流程时调用
        
        Args:
            name: 流程名称
        """
        try:
            # 获取流程管理器
            workflow_manager = get_workflow_manager()
            
            # 删除流程
            workflow_manager.delete_workflow(name)
            
            self.set_status(f"已删除流程: {name}", is_error=False)
            
        except Exception as e:
            self.set_status(f"删除失败: {str(e)}", is_error=True)
            
    def _on_rename_workflow_confirmed(self, old_name, new_name):
        """
        当确认重命名流程时调用
        
        Args:
            old_name: 旧的流程名称
            new_name: 新的流程名称
        """
        try:
            # 获取流程管理器
            workflow_manager = get_workflow_manager()
            
            # 加载旧的配置
            controls_config = workflow_manager.load_workflow(old_name)
            
            if controls_config is not None:
                # 保存为新名称
                workflow_manager.save_workflow(new_name, controls_config)
                # 删除旧的配置
                workflow_manager.delete_workflow(old_name)
                
                self.set_status(f"已重命名流程: {old_name} → {new_name}", is_error=False)
            else:
                self.set_status(f"重命名失败: 流程 '{old_name}' 不存在", is_error=True)
            
        except Exception as e:
            self.set_status(f"重命名失败: {str(e)}", is_error=True)
                
    def set_tab_title(self, title):
        """
        设置标签页标题（通过信号通知父窗口）
        
        Args:
            title: 新的标题
        """
        # 更新内部属性
        self.set_current_tab_name(title)
        # 发出信号
        self.update_tab_title_requested.emit(title)
        
    def _on_save_clicked(self):
        """
        当点击 SAVE/UPDATE 按钮时调用
        保存或更新流程配置
        """
        current_name = self.get_current_tab_name()
        
        if current_name != "[未命名]":
            # 已保存的流程，显示确认对话框
            from PySide6.QtWidgets import QMessageBox, QPushButton
            
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("确认更新")
            msg_box.setText(f"确定要更新流程 '{current_name}' 吗？")
            msg_box.setIcon(QMessageBox.Question)
            
            # 添加按钮
            no_button = msg_box.addButton("取消", QMessageBox.NoRole)
            yes_button = msg_box.addButton("确定", QMessageBox.YesRole)
            
            msg_box.exec()
            
            if msg_box.clickedButton() == yes_button:
                # 用户确认更新
                self._on_save_workflow_confirmed(current_name)
        else:
            # 未保存的流程，显示输入对话框
            # 获取流程管理器
            workflow_manager = get_workflow_manager()
            
            # 获取已存在的流程名称
            existing_names = workflow_manager.get_workflow_names()
            
            # 创建保存对话框
            dialog = SaveWorkflowDialog(existing_names, current_name, self)
            
            # 连接信号
            def on_save_confirmed(name):
                self._on_save_workflow_confirmed(name)
            
            dialog.save_confirmed.connect(on_save_confirmed)
            
            # 显示对话框
            dialog.exec()
        
    def _on_save_workflow_confirmed(self, name):
        """
        当确认保存流程时调用
        
        Args:
            name: 流程名称
        """
        try:
            # 获取流程管理器
            workflow_manager = get_workflow_manager()
            
            # 获取控件配置
            controls_config = self.control_panel.get_controls_config()
            
            # 保存流程（新增或更新）
            workflow_manager.save_workflow(name, controls_config)
            
            # 更新标签页标题
            self.set_tab_title(name)
            
            self.set_status(f"已保存流程: {name}", is_error=False)
            
        except Exception as e:
            self.set_status(f"保存失败: {str(e)}", is_error=True)
            
    def set_status(self, message, is_error=False):
        """
        设置状态栏消息
        
        Args:
            message: 要显示的消息
            is_error: 是否是错误消息
        """
        self.status_label.setText(message)
        if is_error:
            self.status_label.setStyleSheet("padding-left: 10px; color: #ff6b6b;")
        else:
            self.status_label.setStyleSheet("padding-left: 10px; color: #51cf66;")
        
    def get_control_panel(self):
        """
        获取控制面板
        
        Returns:
            ControlPanel: 控制面板实例
        """
        return self.control_panel
        
    def get_text_editor(self):
        """
        获取文本编辑器
        
        Returns:
            TextEditor: 文本编辑器实例
        """
        return self.text_editor
        
    def add_control(self, control_widget):
        """
        向控制面板添加控件
        
        Args:
            control_widget: 要添加的控件
        """
        # 添加控件到面板
        self.control_panel.add_control(control_widget)
