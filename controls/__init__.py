# controls 包
# 包含所有可添加的流程控件

from .base_control import BaseControl
from .text_replace import TextReplaceControl
from .json_format import JsonFormatControl
from .json_compress import JsonCompressControl
from .add_text import AddTextControl
from .case_convert import CaseConvertControl
from .text_split import TextSplitControl
from .text_merge import TextMergeControl
from .text_search_delete import TextSearchDeleteControl
from .remove_duplicate import RemoveDuplicateControl
from .remove_empty_lines import RemoveEmptyLinesControl
from .text_trim import TextTrimControl
from .read_excel_column import ReadExcelColumnControl
from .datetime_convert import DatetimeConvertControl
from .random_datetime import RandomDatetimeControl
from .excel_to_json import ExcelToJsonControl
from .random_number import RandomNumberControl
from .html_extract import HtmlExtractControl
from .delete_lines import DeleteLinesControl
from .calculator import CalculatorControl

__all__ = ['BaseControl', 'TextReplaceControl', 'JsonFormatControl', 'JsonCompressControl', 'AddTextControl', 'CaseConvertControl', 'TextSplitControl', 'TextMergeControl', 'TextSearchDeleteControl', 'RemoveDuplicateControl', 'RemoveEmptyLinesControl', 'TextTrimControl',
           'ReadExcelColumnControl', 'DatetimeConvertControl', 'RandomDatetimeControl', 'ExcelToJsonControl', 'RandomNumberControl', 'HtmlExtractControl', 'DeleteLinesControl', 'CalculatorControl']
