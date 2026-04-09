# -*- coding: utf-8 -*-
"""
文本编辑器模块
提供带行号的代码编辑功能
"""

import re
from PySide6.QtCore import Qt, Signal, QRect, QSize
from PySide6.QtGui import QPainter, QColor, QTextFormat, QTextCursor
from PySide6.QtWidgets import QWidget, QHBoxLayout, QTextEdit
# 导入自定义 PlainTextEdit
from components.custom_text_edit import CustomPlainTextEdit

# 导入语法高亮器
from components.syntax_highlighter import PygmentsHighlighter


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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 创建文本编辑框
        self.text_edit = CodeEditor()
        self.text_edit.setObjectName("TextEditWidget")

        # 连接文本改变信号
        self.text_edit.textChanged.connect(self._on_text_changed)

        # 将文本编辑框添加到布局
        layout.addWidget(self.text_edit)

        # 默认开启自动换行
        from PySide6.QtWidgets import QPlainTextEdit
        self.text_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)

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

    def zoom_in(self):
        """
        放大字体
        """
        self.text_edit.zoom_in()

    def zoom_out(self):
        """
        缩小字体
        """
        self.text_edit.zoom_out()

    def get_font_size(self):
        """
        获取当前字体大小

        Returns:
            int: 字体大小
        """
        return self.text_edit.get_font_size()

    def set_language(self, language):
        """
        设置语法高亮语言

        Args:
            language: 语言名称（text 表示 Plain Text，无高亮）
        """
        self.text_edit.set_language(language)

    def get_language(self):
        """
        获取当前语法高亮语言

        Returns:
            str: 当前语言名称
        """
        return self.text_edit.get_language()

    def find_all(self, pattern, case_sensitive=True, use_regex=False):
        """
        查找所有匹配项

        Args:
            pattern: 搜索模式
            case_sensitive: 是否区分大小写
            use_regex: 是否使用正则表达式

        Returns:
            int: 匹配总数
        """
        # 保存当前搜索参数
        self.text_edit._current_search_pattern = pattern
        self.text_edit._current_case_sensitive = case_sensitive
        self.text_edit._current_use_regex = use_regex
        return self.text_edit.find_all(pattern, case_sensitive, use_regex)

    def find_next(self):
        """
        跳到下一个匹配项

        Returns:
            bool: 是否成功
        """
        return self.text_edit.find_next()

    def find_previous(self):
        """
        跳到上一个匹配项

        Returns:
            bool: 是否成功
        """
        return self.text_edit.find_previous()

    def replace_current(self, replace_str):
        """
        替换当前匹配项

        Args:
            replace_str: 替换文本

        Returns:
            bool: 是否成功
        """
        return self.text_edit.replace_current(replace_str)

    def replace_all(self, replace_str):
        """
        替换所有匹配项

        Args:
            replace_str: 替换文本

        Returns:
            int: 替换数量
        """
        return self.text_edit.replace_all(replace_str)

    def get_current_match_index(self):
        """
        获取当前匹配项索引

        Returns:
            int: 当前索引(从0开始)，没有匹配返回-1
        """
        return self.text_edit.get_current_match_index()

    def get_match_count(self):
        """
        获取匹配总数

        Returns:
            int: 匹配总数
        """
        return self.text_edit.get_match_count()

    def clear_search_highlight(self):
        """清除搜索高亮"""
        self.text_edit.find_all("")

    def set_line_wrap(self, enabled):
        """
        设置自动换行状态

        Args:
            enabled: True 开启自动换行，False 关闭自动换行
        """
        from PySide6.QtWidgets import QPlainTextEdit
        if enabled:
            self.text_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        else:
            self.text_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

    def toggle_line_wrap(self):
        """切换自动换行状态"""
        current_enabled = self.is_line_wrap_enabled()
        self.set_line_wrap(not current_enabled)
        return not current_enabled

    def is_line_wrap_enabled(self):
        """
        获取当前自动换行状态

        Returns:
            bool: True 已开启自动换行，False 已关闭
        """
        from PySide6.QtWidgets import QPlainTextEdit
        return self.text_edit.lineWrapMode() == QPlainTextEdit.LineWrapMode.WidgetWidth


class CodeEditor(CustomPlainTextEdit):
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

        # 初始化语法高亮器（默认 Plain Text，无高亮）
        self.highlighter = PygmentsHighlighter(self.document(), language='text')

        # 连接信号
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        # 初始化行号区域宽度
        self.update_line_number_area_width(0)

        # 初始高亮当前行
        self.highlight_current_line()

        # 字体大小
        self._font_size = 16
        font = self.font()
        font.setPointSize(self._font_size)
        self.setFont(font)
        self.update_line_number_area_width(0)

        # 搜索相关属性
        self._matches = []  # 存储所有匹配项 (start, end) 位置
        self._current_match_index = -1  # 当前选中的匹配项索引

    def line_number_area_width(self):
        """
        计算行号区域需要的宽度

        Returns:
            int: 宽度（像素）
        """
        # 左侧冗余边距
        left_padding = 10

        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1

        # 确保至少能显示3位数字的宽度
        digits = max(digits, 3)

        # 计算宽度：左边距 + 数字宽度 + 右边距
        space = left_padding + self.fontMetrics().horizontalAdvance('9') * digits + 3
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

        # 左侧冗余边距
        left_padding = 10

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor("#606366"))
                # 从左侧边距开始绘制，右边保留8像素间距
                painter.drawText(left_padding, int(top), self.line_number_area.width() - left_padding - 8,
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
        # 获取现有的extra selections
        all_selections = list(self.extraSelections())
        extra_selections = []

        # 只保留搜索相关的高亮，移除所有行高亮
        for s in all_selections:
            # 判断是否是搜索匹配高亮：没有_is_current_line_highlight标记，且背景色不是当前行颜色
            if hasattr(s, '_is_current_line_highlight'):
                continue
            # 检查背景色，排除当前行高亮（可能旧的没有标记）
            bg_color = s.format.background().color()
            if bg_color.name() == "#3c3f41":
                continue
            extra_selections.append(s)

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection._is_current_line_highlight = True  # 标记为当前行高亮

            # 当前行背景色
            line_color = QColor("#3c3f41")
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.insert(0, selection)  # 插入到最前面

        self.setExtraSelections(extra_selections)

    def zoom_in(self):
        """
        放大字体
        """
        self._font_size += 2
        if self._font_size > 72:
            self._font_size = 72
        font = self.font()
        font.setPointSize(self._font_size)
        self.setFont(font)
        self.update_line_number_area_width(0)

    def zoom_out(self):
        """
        缩小字体
        """
        self._font_size -= 2
        if self._font_size < 8:
            self._font_size = 8
        font = self.font()
        font.setPointSize(self._font_size)
        self.setFont(font)
        self.update_line_number_area_width(0)

    def get_font_size(self):
        """
        获取当前字体大小

        Returns:
            int: 字体大小
        """
        return self._font_size

    def set_language(self, language):
        """
        设置语法高亮语言

        Args:
            language: 语言名称（text 表示 Plain Text，无高亮）
        """
        if self.highlighter:
            self.highlighter.set_language(language)

    def get_language(self):
        """
        获取当前语法高亮语言

        Returns:
            str: 当前语言名称
        """
        if self.highlighter:
            return self.highlighter.language
        return 'text'

    def find_all(self, pattern, case_sensitive=True, use_regex=False):
        """
        查找所有匹配项

        Args:
            pattern: 搜索模式
            case_sensitive: 是否区分大小写
            use_regex: 是否使用正则表达式

        Returns:
            int: 匹配总数
        """
        self._matches.clear()
        self._current_match_index = -1

        if not pattern:
            self.highlight_matches()
            return 0

        text = self.toPlainText()
        flags = 0
        if not case_sensitive:
            flags |= re.IGNORECASE

        try:
            if use_regex:
                regex = re.compile(pattern, flags)
            else:
                regex = re.compile(re.escape(pattern), flags)
        except re.error:
            # 正则表达式语法错误
            self.highlight_matches()
            return 0

        for match in regex.finditer(text):
            self._matches.append((match.start(), match.end()))

        if self._matches:
            self._current_match_index = 0
        else:
            self._current_match_index = -1

        # 无论有没有匹配都要更新高亮，清空旧的匹配
        self.highlight_matches()
        return len(self._matches)

    def highlight_matches(self):
        """高亮所有匹配项"""
        extra_selections = []

        # 保留原有的当前行高亮
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor("#3c3f41")
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        # 高亮所有匹配项
        for i, (start, end) in enumerate(self._matches):
            selection = QTextEdit.ExtraSelection()
            cursor = self.textCursor()
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.KeepAnchor)
            selection.cursor = cursor

            if i == self._current_match_index:
                # 当前匹配项：淡橘色
                selection.format.setBackground(QColor("#ffd3b6"))
                selection.format.setForeground(QColor("#000000"))
            else:
                # 其他匹配项：淡蓝灰色
                selection.format.setBackground(QColor("#a9c4eb"))
                selection.format.setForeground(QColor("#000000"))

            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def find_next(self):
        """
        跳到下一个匹配项

        Returns:
            bool: 是否成功
        """
        if not self._matches:
            return False

        self._current_match_index = (self._current_match_index + 1) % len(self._matches)
        self.highlight_matches()

        # 只滚动到可见区域，不移动光标
        if self._current_match_index >= 0:
            start, _ = self._matches[self._current_match_index]
            # 滚动到匹配项位置但不改变光标
            cursor = self.textCursor()
            original_pos = cursor.position()
            cursor.setPosition(start)
            self.setTextCursor(cursor)
            self.ensureCursorVisible()
            # 恢复原光标位置
            cursor.setPosition(original_pos)
            self.setTextCursor(cursor)

        return True

    def find_previous(self):
        """
        跳到上一个匹配项

        Returns:
            bool: 是否成功
        """
        if not self._matches:
            return False

        self._current_match_index = (self._current_match_index - 1) % len(self._matches)
        self.highlight_matches()

        # 只滚动到可见区域，不移动光标
        if self._current_match_index >= 0:
            start, _ = self._matches[self._current_match_index]
            # 滚动到匹配项位置但不改变光标
            cursor = self.textCursor()
            original_pos = cursor.position()
            cursor.setPosition(start)
            self.setTextCursor(cursor)
            self.ensureCursorVisible()
            # 恢复原光标位置
            cursor.setPosition(original_pos)
            self.setTextCursor(cursor)

        return True

    def replace_current(self, replace_str):
        """
        替换当前匹配项

        Args:
            replace_str: 替换文本

        Returns:
            bool: 是否成功
        """
        if self._current_match_index < 0 or self._current_match_index >= len(self._matches):
            return False

        # 获取当前匹配项位置
        start, end = self._matches[self._current_match_index]

        # 替换文本
        cursor = self.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        cursor.insertText(replace_str)

        # 重新搜索，因为文本已经变化
        pattern = self._current_search_pattern if hasattr(self, '_current_search_pattern') else ""
        case_sensitive = self._current_case_sensitive if hasattr(self, '_current_case_sensitive') else True
        use_regex = self._current_use_regex if hasattr(self, '_current_use_regex') else False

        # 保存当前搜索参数用于重新搜索
        self._current_search_pattern = pattern
        self._current_case_sensitive = case_sensitive
        self._current_use_regex = use_regex

        total = self.find_all(pattern, case_sensitive, use_regex)
        return total > 0

    def replace_all(self, replace_str):
        """
        替换所有匹配项

        Args:
            replace_str: 替换文本

        Returns:
            int: 替换数量
        """
        if not self._matches:
            return 0

        # 临时保存匹配项副本，避免替换过程中被信号修改
        matches = list(self._matches)
        # 从后往前替换，避免位置偏移
        matches.sort(reverse=True, key=lambda x: x[0])

        # 临时阻塞信号，避免替换过程中触发自动搜索
        self.blockSignals(True)

        cursor = self.textCursor()
        cursor.beginEditBlock()  # 开始编辑块，支持撤销

        count = 0
        try:
            for start, end in matches:
                cursor.setPosition(start)
                cursor.setPosition(end, QTextCursor.KeepAnchor)
                cursor.insertText(replace_str)
                count += 1
        finally:
            cursor.endEditBlock()  # 结束编辑块
            self.blockSignals(False)

        self._matches.clear()
        self._current_match_index = -1
        self.highlight_matches()
        return count

    def get_current_match_index(self):
        """
        获取当前匹配项索引

        Returns:
            int: 当前索引(从0开始)，没有匹配返回-1
        """
        return self._current_match_index

    def get_match_count(self):
        """
        获取匹配总数

        Returns:
            int: 匹配总数
        """
        return len(self._matches)