"""
Основные классы для обработки PDF документов
"""

import os
import re
import cv2
import fitz
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import easyocr
from pathlib import Path
import pdfplumber
import spacy
import nltk
from typing import List, Dict, Tuple, Optional, Union
import json
import yaml
from datetime import datetime
import logging
import time
from dataclasses import dataclass
from enum import Enum
import tempfile
# from .enhanced_processor import EnhancedPDFProcessor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QualityLevel(Enum):
    A = "excellent"
    B = "good"
    C = "medium" 
    D = "poor"

@dataclass
class DocumentMetadata:
    filename: str
    pages_count: int
    quality_level: QualityLevel
    confidence_score: float
    processing_method: str
    creation_date: str
    file_size: int

@dataclass
class ExtractedBlock:
    text: str
    block_type: str
    level: int
    confidence: float
    page_number: int
    bbox: Optional[Tuple[float, float, float, float]] = None

class FileUploader:
    def __init__(self):
        self.uploaded_files = {}
        self.temp_dir = tempfile.mkdtemp()

    def upload_files(self) -> Dict[str, str]:
        print("📁 Выберите PDF файлы для анализа:")
        print("Поддерживаются файлы: .pdf")
        print("Можно загружать несколько файлов одновременно\n")

        try:
            from google.colab import files
            uploaded = files.upload()
        except ImportError:
            print("❌ Google Colab не доступен")
            return {}

        if not uploaded:
            print("❌ Файлы не были загружены")
            return {}

        file_paths = {}
        for filename, data in uploaded.items():
            if not filename.lower().endswith('.pdf'):
                print(f"⚠️ Пропускаем файл {filename} - поддерживаются только PDF")
                continue

            file_path = os.path.join(self.temp_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(data)

            file_paths[filename] = file_path
            file_size = len(data)
            print(f"✅ Загружен: {filename} ({file_size / 1024:.1f} KB)")

        self.uploaded_files = file_paths
        if file_paths:
            print(f"\n📋 Всего загружено файлов: {len(file_paths)}")
            print("Готово к обработке!")

        return file_paths

# Добавим остальные классы в следующей ячейке...


class PDFQualityAnalyzer:
    def __init__(self):
        self.text_threshold = 100

    def analyze_pdf_quality(self, pdf_path: str) -> Tuple[QualityLevel, float, str]:
        try:
            doc = fitz.open(pdf_path)
            total_text_length = 0
            has_text_layer = False
            sample_pages = min(3, len(doc))

            for page_num in range(sample_pages):
                page = doc[page_num]
                text = page.get_text()
                total_text_length += len(text.strip())
                if len(text.strip()) > 50:
                    has_text_layer = True

            doc.close()

            if has_text_layer and total_text_length > self.text_threshold * sample_pages:
                return QualityLevel.A, 0.95, "text_extraction"

            return self._analyze_image_quality(pdf_path)

        except Exception as e:
            logger.error(f"Ошибка анализа PDF {pdf_path}: {e}")
            return QualityLevel.D, 0.3, "ocr_advanced"

    def _analyze_image_quality(self, pdf_path: str) -> Tuple[QualityLevel, float, str]:
        try:
            doc = fitz.open(pdf_path)
            quality_scores = []

            for page_num in range(min(2, len(doc))):
                page = doc[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_data = pix.tobytes("png")
                nparr = np.frombuffer(img_data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

                if img is not None:
                    score = self._calculate_image_quality_score(img)
                    quality_scores.append(score)

            doc.close()

            if not quality_scores:
                return QualityLevel.D, 0.3, "ocr_advanced"

            avg_score = sum(quality_scores) / len(quality_scores)

            if avg_score > 0.8:
                return QualityLevel.B, avg_score, "ocr_simple"
            elif avg_score > 0.6:
                return QualityLevel.C, avg_score, "ocr_enhanced"
            else:
                return QualityLevel.D, avg_score, "ocr_advanced"

        except Exception as e:
            logger.error(f"Ошибка анализа изображений: {e}")
            return QualityLevel.D, 0.3, "ocr_advanced"

    def _calculate_image_quality_score(self, img: np.ndarray) -> float:
        laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
        sharpness_score = min(laplacian_var / 1000, 1.0)

        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        contrast_score = hist.std() / 128.0

        mean_brightness = img.mean()
        brightness_score = 1.0 - abs(mean_brightness - 127) / 127.0

        total_score = (sharpness_score * 0.4 + contrast_score * 0.4 + brightness_score * 0.2)
        return min(total_score, 1.0)


class AdvancedPDFExtractProcessor:
    def __init__(self):
        self.quality_analyzer = PDFQualityAnalyzer()
        self.file_uploader = FileUploader()
        
        self.processing_stats = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'total_pages': 0,
            'average_confidence': 0.0,
            'processing_time': 0.0
        }

    def interactive_process_advanced(self) -> Dict[str, str]:
        print("🚀 ПРОДВИНУТАЯ СИСТЕМА ИЗВЛЕЧЕНИЯ ТЕКСТА ИЗ PDF")
        print("=" * 70)
        
        file_paths = self.file_uploader.upload_files()
        
        if not file_paths:
            return {}
            
        results = {}
        start_time = time.time()
        
        for i, (filename, file_path) in enumerate(file_paths.items(), 1):
            print(f"\n📄 [{i}/{len(file_paths)}] Обработка: {filename}")
            print("-" * 60)
            
            try:
                result = self.process_single_file_advanced(file_path)
                if result:
                    output_filename = f"{os.path.splitext(filename)[0]}_processed.md"
                    results[filename] = {
                        'markdown_content': result,
                        'output_filename': output_filename,
                        'status': 'success'
                    }
                    print(f"✅ Успешно обработан: {filename}")
                else:
                    results[filename] = {'status': 'failed'}
                    print(f"❌ Ошибка обработки: {filename}")
                    
            except Exception as e:
                logger.error(f"Ошибка обработки {filename}: {e}")
                results[filename] = {'status': 'error', 'error': str(e)}
                
        total_time = time.time() - start_time
        self._print_summary(results, total_time)
        
        return results

    def process_single_file_advanced(self, file_path: str) -> Optional[str]:
        try:
            print("🔍 Анализ качества...")
            quality_level, confidence, method = self.quality_analyzer.analyze_pdf_quality(file_path)
            
            print(f"   📊 Качество: {quality_level.value}")
            print(f"   📈 Уверенность: {confidence:.3f}")
            
            # Простое извлечение текста для демонстрации
            print("📝 Извлечение текста...")
            
            doc = fitz.open(file_path)
            full_text = ""
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                full_text += f"\n\n--- Страница {page_num + 1} ---\n\n{text}"
                
            doc.close()
            
            # Создаем простой Markdown
            markdown_content = f"""# Извлеченный текст

**Файл:** {os.path.basename(file_path)}
**Качество:** {quality_level.value}
**Метод:** {method}
**Уверенность:** {confidence:.3f}

---

{full_text}

---

*Обработано системой PDF Extract Processor v2.0*
"""
            
            return markdown_content
            
        except Exception as e:
            logger.error(f"Ошибка обработки {file_path}: {e}")
            return None

    def _print_summary(self, results: Dict, total_time: float):
        print("\n" + "=" * 60)
        print("📊 СТАТИСТИКА ОБРАБОТКИ")
        print("=" * 60)
        
        successful = sum(1 for r in results.values() if r.get('status') == 'success')
        print(f"✅ Успешно: {successful}/{len(results)}")
        print(f"⏱️ Время: {total_time:.1f}с")

    def auto_process_with_detection(self, pdf_path):
        """Автоматическая обработка с определением метода"""
        enhanced = EnhancedPDFProcessor()
        result = enhanced.extract_with_auto_method(pdf_path)
        
        # Возвращаем в формате, совместимом с существующими методами
        if 'content' in result:
            return {
                'markdown_content': result['content'],
                'processing_method': result.get('method', 'unknown'),
                'quality_score': result.get('confidence', 0.5),
                'processing_stats': {
                    'pages_processed': result.get('pages_processed', 0),
                    'characters_extracted': result.get('characters', 0)
                }
            }
        else:
            return {'error': result.get('error', 'Unknown error')}
# Standalone version for testing
