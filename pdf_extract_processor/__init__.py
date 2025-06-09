"""
Extract_Processor - Улучшенная система извлечения PDF
Версия 2.0 с премиум постобработкой и RAG-инструментами
"""

__version__ = "2.0"

from .main_processor import AdvancedPDFExtractProcessor
from .improved_processor import ImprovedAdvancedPDFExtractProcessor
from .quality_analyzer import IndependentQualityAnalyzer

# Новые модули
try:
    from .postprocessing.premium_processor import PremiumPostProcessor
    from .rag_tools.rag_processor import RAGDataProcessor
except ImportError:
    # Обратная совместимость
    PremiumPostProcessor = None
    RAGDataProcessor = None

__all__ = [
    'AdvancedPDFExtractProcessor',
    'ImprovedAdvancedPDFExtractProcessor', 
    'IndependentQualityAnalyzer',
    'PremiumPostProcessor',
    'RAGDataProcessor'
]

# Улучшенные компоненты
from .enhanced_processor import EnhancedPDFProcessor, diagnose_multiple_pdfs
from .utils.diagnostics import quick_pdf_test, analyze_pdf_batch, print_batch_analysis
