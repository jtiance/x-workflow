# -*- coding: utf-8 -*-
"""
语法高亮器模块
使用 Pygments 和 QSyntaxHighlighter 实现多语言语法高亮
"""

from PySide6.QtGui import (
    QSyntaxHighlighter, QTextCharFormat, QColor, QFont
)
from pygments import lex
from pygments.lexers import (
    JsonLexer, SqlLexer, XmlLexer, HtmlLexer, YamlLexer,
    get_lexer_by_name, get_lexer_for_mimetype, TextLexer
)
from pygments.token import Token


class PygmentsHighlighter(QSyntaxHighlighter):
    """
    基于 Pygments 的通用语法高亮器

    支持的语言：
    - Plain Text（无高亮）
    - JSON
    - SQL
    - XML
    - HTML
    - YAML
    - 以及 Pygments 支持的所有其他语言
    """

    def __init__(self, document, language='text'):
        """
        初始化语法高亮器

        Args:
            document: QTextDocument 实例
            language: 语言名称（text, json, sql, xml, html, yaml 等）
        """
        super().__init__(document)
        self.language = language
        self.lexer = self._get_lexer(language)
        self._init_formats()

    def _get_lexer(self, language):
        """
        根据语言名称获取对应的 Pygments lexer

        Args:
            language: 语言名称

        Returns:
            Pygments lexer 实例
        """
        # 如果是 'text'（Plain Text），返回 TextLexer（无高亮）
        if language == 'text':
            return TextLexer()

        language_map = {
            'json': JsonLexer,
            'sql': SqlLexer,
            'xml': XmlLexer,
            'html': HtmlLexer,
            'yaml': YamlLexer,
            'yml': YamlLexer,
        }

        lexer_class = language_map.get(language.lower())
        if lexer_class:
            return lexer_class()

        # 如果找不到对应的 lexer，返回 TextLexer（无高亮）
        return TextLexer()

    def _init_formats(self):
        """
        初始化 token 到格式的映射

        使用 VS Code Dark+ 风格的配色方案
        """
        self.formats = {
            # 关键字（紫色）
            Token.Keyword: self._create_format("#C586C0", bold=True),
            Token.Keyword.Constant: self._create_format("#569CD6"),
            Token.Keyword.Type: self._create_format("#569CD6"),
            Token.Keyword.Declaration: self._create_format("#569CD6"),
            Token.Keyword.Namespace: self._create_format("#569CD6"),

            Token.Keyword.Pseudo: self._create_format("#C586C0"),
            Token.Keyword.Reserved: self._create_format("#C586C0"),

            # 名称（浅蓝色）
            Token.Name: self._create_format("#9CDCFE"),
            Token.Name.Attribute: self._create_format("#9CDCFE"),
            Token.Name.Tag: self._create_format("#569CD6", bold=True),
            Token.Name.Label: self._create_format("#9CDCFE"),
            Token.Name.Entity: self._create_format("#4EC9B0"),
            Token.Name.Variable: self._create_format("#9CDCFE"),
            Token.Name.Function: self._create_format("#DCDCAA"),
            Token.Name.Class: self._create_format("#4EC9B0"),
            Token.Name.Constant: self._create_format("#9CDCFE"),
            Token.Name.Builtin: self._create_format("#4EC9B0"),
            Token.Name.Builtin.Pseudo: self._create_format("#9CDCFE"),

            # 字符串（橙色）
            Token.String: self._create_format("#CE9178"),
            Token.String.Single: self._create_format("#CE9178"),
            Token.String.Double: self._create_format("#CE9178"),
            Token.String.Backtick: self._create_format("#CE9178"),
            Token.String.Char: self._create_format("#CE9178"),
            Token.String.Doc: self._create_format("#CE9178"),

            # 数字（浅绿色）
            Token.Number: self._create_format("#B5CEA8"),
            Token.Number.Integer: self._create_format("#B5CEA8"),
            Token.Number.Float: self._create_format("#B5CEA8"),
            Token.Number.Hex: self._create_format("#B5CEA8"),
            Token.Number.Oct: self._create_format("#B5CEA8"),

            # 注释（绿色）
            Token.Comment: self._create_format("#6A9955", italic=True),
            Token.Comment.Single: self._create_format("#6A9955", italic=True),
            Token.Comment.Multiline: self._create_format("#6A9955", italic=True),
            Token.Comment.Preproc: self._create_format("#6A9955", italic=True),
            Token.Comment.Special: self._create_format("#6A9955", italic=True),

            # 操作符（白色）
            Token.Operator: self._create_format("#D4D4D4"),
            Token.Operator.Word: self._create_format("#C586C0"),

            # 标点符号（白色）
            Token.Punctuation: self._create_format("#D4D4D4"),

            # 错误（红色）
            Token.Error: self._create_format("#F44747"),

            # 通用（浅蓝色）
            Token.Generic: self._create_format("#9CDCFE"),
            Token.Generic.Heading: self._create_format("#4EC9B0", bold=True),
            Token.Generic.Subheading: self._create_format("#4EC9B0"),
            Token.Generic.Emph: self._create_format("#9CDCFE"),
            Token.Generic.Strong: self._create_format("#9CDCFE", bold=True),
            Token.Generic.Prompt: self._create_format("#9CDCFE"),
            Token.Generic.Output: self._create_format("#9CDCFE"),
            Token.Generic.Traceback: self._create_format("#F44747"),
        }

    def _create_format(self, color, bold=False, italic=False):
        """
        创建 QTextCharFormat

        Args:
            color: 颜色（十六进制字符串）
            bold: 是否粗体
            italic: 是否斜体

        Returns:
            QTextCharFormat 实例
        """
        format = QTextCharFormat()
        format.setForeground(QColor(color))

        if bold:
            format.setFontWeight(QFont.Bold)
        if italic:
            format.setFontItalic(True)

        return format

    def highlightBlock(self, text):
        """
        高亮一个文本块

        Args:
            text: 要高亮的文本
        """
        # 如果语言是 'text'（Plain Text），不进行高亮
        if self.language == 'text':
            return

        # 使用 Pygments 对文本进行词法分析
        for token_type, value in lex(text, self.lexer):
            # 获取对应的格式
            format = self.formats.get(token_type)

            if format:
                # 找到 value 在 text 中的位置
                # 注意：这里需要准确匹配，因为 value 可能包含特殊字符
                start = text.find(value)
                if start != -1:
                    self.setFormat(start, len(value), format)
                    # 替换已处理的部分，避免重复匹配
                    text = text[:start] + ' ' * len(value) + text[start + len(value):]

    def set_language(self, language):
        """
        切换语言

        Args:
            language: 语言名称（text 表示 Plain Text，无高亮）
        """
        self.language = language
        self.lexer = self._get_lexer(language)
        # 触发重新高亮
        self.rehighlight()


class SyntaxHighlighterFactory:
    """
    语法高亮器工厂类

    用于创建和管理语法高亮器实例
    """

    @staticmethod
    def create(document, language='text'):
        """
        创建语法高亮器

        Args:
            document: QTextDocument 实例
            language: 语言名称

        Returns:
            PygmentsHighlighter 实例
        """
        return PygmentsHighlighter(document, language)

    @staticmethod
    def supported_languages():
        """
        获取支持的语言列表

        Returns:
            list: 支持的语言名称列表
        """
        return ['text', 'json', 'sql', 'xml', 'html', 'yaml', 'yml']

    @staticmethod
    def is_supported(language):
        """
        检查语言是否支持

        Args:
            language: 语言名称

        Returns:
            bool: 是否支持
        """
        return language.lower() in SyntaxHighlighterFactory.supported_languages()