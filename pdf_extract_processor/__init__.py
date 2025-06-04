"""
PDF Extract Processor - Продвинутая система извлечения текста из PDF

Версия: 2.0.0
Автор: PDF Extract Processor Team
"""

__version__ = "2.0.0"
__author__ = "PDF Extract Processor Team"
__email__ = "contact@pdfextract.com"

# Импорты основных классов
from .main_processor import AdvancedPDFExtractProcessor
from .quality_analyzer import IndependentQualityAnalyzer

__all__ = [
    "AdvancedPDFExtractProcessor",
    "IndependentQualityAnalyzer",
]
