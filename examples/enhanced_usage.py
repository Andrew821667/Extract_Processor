"""
Пример использования улучшенного Extract_Processor v2.0
"""

import sys
sys.path.append('/content/Extract_Processor')

from pdf_extract_processor import AdvancedPDFExtractProcessor
from pdf_extract_processor.postprocessing.premium_processor import PremiumPostProcessor
from pdf_extract_processor.rag_tools.rag_processor import RAGDataProcessor

def example_enhanced_processing():
    """Пример улучшенной обработки PDF"""
    
    # 1. Основное извлечение
    processor = AdvancedPDFExtractProcessor()
    
    # 2. Постобработка
    postprocessor = PremiumPostProcessor()
    
    # 3. RAG подготовка
    rag_processor = RAGDataProcessor()
    
    # Пример обработки
    pdf_file = "example.pdf"
    
    # Извлекаем
    raw_result = processor.process_single_file_advanced(pdf_file)
    
    # Постобрабатываем
    enhanced_text = postprocessor.process(str(raw_result))
    
    # Готовим для RAG
    rag_ready = rag_processor.clean_npa_for_rag(enhanced_text)
    
    return {
        'raw': raw_result,
        'enhanced': enhanced_text,
        'rag_ready': rag_ready
    }

if __name__ == "__main__":
    result = example_enhanced_processing()
    print("✅ Пример работает!")
