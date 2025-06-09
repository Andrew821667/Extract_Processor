"""
Улучшенный процессор PDF с автоматическим OCR и диагностикой
Добавлено для решения проблем с сканированными документами
"""

import os
import fitz
from PIL import Image
import pytesseract
import io
from typing import Dict, List, Tuple, Optional

class EnhancedPDFProcessor:
    """Улучшенный процессор с автоматическим определением OCR"""
    
    def __init__(self):
        self.name = "EnhancedPDFProcessor"
        self.ocr_threshold = 50  # Минимум символов для считания текста извлеченным
        
    def diagnose_pdf(self, pdf_path: str) -> Dict:
        """Диагностика PDF файла для определения метода обработки"""
        try:
            doc = fitz.open(pdf_path)
            
            diagnosis = {
                'filename': os.path.basename(pdf_path),
                'pages': len(doc),
                'encrypted': doc.needs_pass,
                'metadata': doc.metadata,
                'requires_ocr': False,
                'extractable_text': 0,
                'quality': 'unknown'
            }
            
            # Проверяем первые 3 страницы на наличие текста
            text_samples = []
            for page_num in range(min(3, len(doc))):
                page = doc.load_page(page_num)
                text = page.get_text()
                text_samples.append(len(text.strip()))
            
            diagnosis['extractable_text'] = sum(text_samples)
            
            # Определяем нужен ли OCR
            if diagnosis['extractable_text'] < self.ocr_threshold:
                diagnosis['requires_ocr'] = True
                diagnosis['quality'] = 'scanned_image'
            else:
                diagnosis['requires_ocr'] = False
                diagnosis['quality'] = 'text_extractable'
            
            doc.close()
            return diagnosis
            
        except Exception as e:
            return {
                'filename': os.path.basename(pdf_path),
                'error': str(e),
                'requires_ocr': True,
                'quality': 'error'
            }
    
    def extract_with_auto_method(self, pdf_path: str) -> Dict:
        """Автоматическое извлечение с выбором оптимального метода"""
        diagnosis = self.diagnose_pdf(pdf_path)
        
        if diagnosis.get('requires_ocr', False):
            return self.extract_with_ocr(pdf_path, diagnosis)
        else:
            return self.extract_direct_text(pdf_path, diagnosis)
    
    def extract_direct_text(self, pdf_path: str, diagnosis: Dict) -> Dict:
        """Прямое извлечение текста"""
        try:
            doc = fitz.open(pdf_path)
            content_parts = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                
                if text.strip():
                    content_parts.append(f"\n## Страница {page_num + 1}\n\n{text}")
            
            doc.close()
            
            result_content = "\n".join(content_parts)
            
            return {
                'method': 'direct_text_extraction',
                'quality': diagnosis.get('quality', 'good'),
                'confidence': 0.95,
                'content': result_content,
                'pages_processed': len(content_parts),
                'characters': len(result_content)
            }
            
        except Exception as e:
            return {'error': str(e), 'method': 'direct_text_extraction'}
    
    def extract_with_ocr(self, pdf_path: str, diagnosis: Dict) -> Dict:
        """OCR извлечение для сканированных PDF"""
        try:
            doc = fitz.open(pdf_path)
            content_parts = []
            
            # Ограничиваем количество страниц для OCR (производительность)
            max_pages = min(len(doc), 50)
            
            for page_num in range(max_pages):
                page = doc.load_page(page_num)
                
                # Сначала пробуем прямое извлечение
                direct_text = page.get_text()
                if len(direct_text.strip()) > self.ocr_threshold:
                    content_parts.append(f"\n## Страница {page_num + 1}\n\n{direct_text}")
                    continue
                
                # Если мало текста - используем OCR
                try:
                    pix = page.get_pixmap()
                    img_data = pix.tobytes("png")
                    image = Image.open(io.BytesIO(img_data))
                    
                    # OCR с русским и английским языками
                    ocr_text = pytesseract.image_to_string(image, lang='rus+eng')
                    
                    if ocr_text.strip():
                        content_parts.append(f"\n## Страница {page_num + 1} (OCR)\n\n{ocr_text}")
                    
                except Exception as ocr_e:
                    content_parts.append(f"\n## Страница {page_num + 1} (Ошибка OCR)\n\nОшибка: {str(ocr_e)}")
            
            doc.close()
            
            result_content = "\n".join(content_parts)
            
            return {
                'method': 'ocr_extraction', 
                'quality': diagnosis.get('quality', 'good'),
                'confidence': 0.85,
                'content': result_content,
                'pages_processed': len(content_parts),
                'characters': len(result_content)
            }
            
        except Exception as e:
            return {'error': str(e), 'method': 'ocr_extraction'}

def diagnose_multiple_pdfs(pdf_paths: List[str]) -> Dict:
    """Диагностика множественных PDF файлов"""
    processor = EnhancedPDFProcessor()
    results = []
    
    for pdf_path in pdf_paths:
        diagnosis = processor.diagnose_pdf(pdf_path)
        results.append(diagnosis)
    
    # Сводная статистика
    total_files = len(results)
    ocr_required = sum(1 for r in results if r.get('requires_ocr', False))
    
    summary = {
        'total_files': total_files,
        'direct_extraction': total_files - ocr_required,
        'ocr_required': ocr_required,
        'files': results
    }
    
    return summary
