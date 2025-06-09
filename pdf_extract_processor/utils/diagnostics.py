"""
Диагностические утилиты для PDF обработки
"""

import os
from typing import List, Dict
from ..enhanced_processor import EnhancedPDFProcessor, diagnose_multiple_pdfs

def quick_pdf_test(pdf_path: str) -> None:
    """Быстрый тест PDF файла"""
    processor = EnhancedPDFProcessor()
    diagnosis = processor.diagnose_pdf(pdf_path)
    
    print(f"📄 Файл: {diagnosis['filename']}")
    print(f"📊 Страниц: {diagnosis.get('pages', 'Неизвестно')}")
    print(f"🔐 Зашифрован: {diagnosis.get('encrypted', False)}")
    print(f"📝 Символов извлечено: {diagnosis.get('extractable_text', 0)}")
    print(f"🔍 Требует OCR: {'Да' if diagnosis.get('requires_ocr') else 'Нет'}")
    print(f"⭐ Качество: {diagnosis.get('quality', 'Неизвестно')}")

def analyze_pdf_batch(pdf_directory: str) -> Dict:
    """Анализ батча PDF файлов"""
    pdf_files = [
        os.path.join(pdf_directory, f) 
        for f in os.listdir(pdf_directory) 
        if f.lower().endswith('.pdf')
    ]
    
    return diagnose_multiple_pdfs(pdf_files)

def print_batch_analysis(analysis: Dict) -> None:
    """Печать результатов анализа батча"""
    print(f"📊 АНАЛИЗ БАТЧА PDF")
    print(f"=" * 30)
    print(f"📄 Всего файлов: {analysis['total_files']}")
    print(f"✅ Прямое извлечение: {analysis['direct_extraction']}")
    print(f"🔍 Требует OCR: {analysis['ocr_required']}")
    
    if analysis['ocr_required'] > 0:
        print(f"\n🔍 Файлы, требующие OCR:")
        for file_info in analysis['files']:
            if file_info.get('requires_ocr'):
                print(f"   - {file_info['filename']}")
