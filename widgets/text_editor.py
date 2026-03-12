# -*- coding: utf-8 -*-
"""
文本编辑器模块
提供带行号的代码编辑功能
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QPlainTextEdit, QTextEdit
from PySide6.QtCore import Qt, Signal, QRect, QSize
from PySide6.QtGui import QPainter, QColor, QTextFormat, QTextCursor


class LineNumberArea(QWidget):
    """
    行号显示区域
    """
    
    def __init__(self, editor):
        """
        初始化行号区域
        
        Args:
            editor: 关联的代码编辑器
        """
        super().__init__(editor)
        self.code_editor = editor
        
    def sizeHint(self):
        """
        返回推荐的尺寸
        """
        return QSize(self.code_editor.line_number_area_width(), 0)
        
    def paintEvent(self, event):
        """
        绘制行号
        """
        self.code_editor.line_number_area_paint_event(event)


class TextEditor(QWidget):
    """
    带行号的文本编辑器组件
    """
    
    # 定义信号：当文本内容改变时发出
    text_changed = Signal(str)
    
    def __init__(self, parent=None):
        """
        初始化文本编辑器
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        
        # 设置控件的对象名称
        self.setObjectName("TextEditor")
        
        # 初始化 UI
        self._init_ui()
        
    def _init_ui(self):
        """
        初始化用户界面
        """
        # 创建主布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 15, 0, 0)  # 上边距15px，右边距0px
        layout.setSpacing(0)
        
        # 创建文本编辑框
        self.text_edit = CodeEditor()
        self.text_edit.setPlaceholderText("在此输入文本...")
        self.text_edit.setObjectName("TextEditWidget")
        
        # 连接文本改变信号
        self.text_edit.textChanged.connect(self._on_text_changed)
        
        # 将文本编辑框添加到布局
        layout.addWidget(self.text_edit)
        
        # 设置大小策略，确保高度一致
        from PySide6.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def _on_text_changed(self):
        """
        当文本内容改变时调用
        发出 text_changed 信号
        """
        text = self.get_text()
        self.text_changed.emit(text)
        
    def get_text(self):
        """
        获取当前文本内容
        
        Returns:
            str: 文本内容
        """
        return self.text_edit.toPlainText()
        
    def set_text(self, text):
        """
        设置文本内容
        
        Args:
            text: 要设置的文本
        """
        self.text_edit.setPlainText(text)
        
    def replace_text(self, find_str, replace_str):
        """
        在文本中替换所有匹配的字符串
        
        Args:
            find_str: 要查找的字符串
            replace_str: 替换的字符串
        """
        # 获取当前文本
        current_text = self.get_text()
        
        # 执行替换
        new_text = current_text.replace(find_str, replace_str)
        
        # 设置新文本
        self.set_text(new_text)
        
    def append_text(self, text):
        """
        在文本末尾追加内容
        
        Args:
            text: 要追加的文本
        """
        self.text_edit.appendPlainText(text)
        
    def clear(self):
        """
        清空文本内容
        """
        self.text_edit.clear()


class CodeEditor(QPlainTextEdit):
    """
    带行号的代码编辑器
    """
    
    def __init__(self, parent=None):
        """
        初始化代码编辑器
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        
        # 创建行号区域
        self.line_number_area = LineNumberArea(self)
        
        # 连接信号
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        
        # 初始化行号区域宽度
        self.update_line_number_area_width(0)
        
        # 初始高亮当前行
        self.highlight_current_line()
        
    def line_number_area_width(self):
        """
        计算行号区域需要的宽度
        
        Returns:
            int: 宽度（像素）
        """
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        
        # 计算宽度：数字宽度 + 边距
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
        
    def update_line_number_area_width(self, new_block_count):
        """
        更新行号区域的宽度
        
        Args:
            new_block_count: 新的块数量（行数）
        """
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
        
    def update_line_number_area(self, rect, dy):
        """
        更新行号区域
        
        Args:
            rect: 需要更新的矩形区域
            dy: 垂直滚动距离
        """
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)
            
    def resizeEvent(self, event):
        """
        处理窗口大小改变事件
        
        Args:
            event: 调整大小事件
        """
        super().resizeEvent(event)
        
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))
        
    def line_number_area_paint_event(self, event):
        """
        绘制行号区域
        
        Args:
            event: 绘制事件
        """
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#2b2b2b"))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor("#606366"))
                painter.drawText(0, int(top), self.line_number_area.width(), 
                                self.fontMetrics().height(),
                                Qt.AlignRight, number)
                
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
            
    def highlight_current_line(self):
        """
        高亮当前行
        """
        extra_selections = []
        
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            
            # 当前行背景色
            line_color = QColor("#3c3f41")
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
            
        self.setExtraSelections(extra_selections)
