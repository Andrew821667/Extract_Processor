"""
Независимый анализатор качества PDF файлов
"""

import os
import time
import logging
from typing import Dict

# Импорт основных классов
from .main_processor import QualityLevel, FileUploader, PDFQualityAnalyzer

logger = logging.getLogger(__name__)

class IndependentQualityAnalyzer:
    def __init__(self):
        self.file_uploader = FileUploader()
        self.quality_analyzer = PDFQualityAnalyzer()
        
        self.quality_thresholds = {
            'text_ratio': 0.8,
            'image_quality': 0.7,
            'table_complexity': 0.6,
            'structure_complexity': 0.5
        }

    def analyze_files_quality(self):
        print("🔍 АНАЛИЗАТОР КАЧЕСТВА PDF ФАЙЛОВ")
        print("=" * 50)
        print("📋 Функции анализатора:")
        print("  • Определение типа PDF (текстовый/сканированный)")
        print("  • Оценка качества и сложности обработки")
        print("  • Рекомендации по методам обработки")
        print("=" * 50)

        file_paths = self.file_uploader.upload_files()

        if not file_paths:
            print("❌ Файлы не были загружены")
            return

        analysis_results = {}
        total_start_time = time.time()

        print(f"\n🔍 Анализирую {len(file_paths)} файлов...")
        print("-" * 50)

        for i, (filename, file_path) in enumerate(file_paths.items(), 1):
            print(f"\n📄 [{i}/{len(file_paths)}] Анализ: {filename}")

            try:
                analysis_start = time.time()
                result = self._analyze_single_file(file_path, filename)
                analysis_time = time.time() - analysis_start

                result['analysis_time'] = analysis_time
                analysis_results[filename] = result

                self._print_file_summary(result)

            except Exception as e:
                logger.error(f"Ошибка анализа {filename}: {e}")
                analysis_results[filename] = {
                    'status': 'error',
                    'error': str(e),
                    'analysis_time': 0
                }
                print(f"❌ Ошибка анализа: {str(e)}")

        total_analysis_time = time.time() - total_start_time
        self._print_detailed_report(analysis_results, total_analysis_time)

        return analysis_results

    def _analyze_single_file(self, file_path: str, filename: str) -> dict:
        result = {
            'filename': filename,
            'file_path': file_path,
            'status': 'success'
        }

        # Анализ качества PDF
        quality_level, confidence, method = self.quality_analyzer.analyze_pdf_quality(file_path)
        
        result.update({
            'quality_level': quality_level,
            'confidence': confidence,
            'recommended_method': method,
            'file_size': os.path.getsize(file_path)
        })

        return result

    def _print_file_summary(self, result: dict):
        if result.get('status') == 'error':
            print(f"❌ {result.get('error', 'Неизвестная ошибка')}")
            return

        quality = result.get('quality_level')
        confidence = result.get('confidence', 0)
        method = result.get('recommended_method', 'unknown')

        quality_emoji = {
            QualityLevel.A: '🟢',
            QualityLevel.B: '🟡', 
            QualityLevel.C: '🟠',
            QualityLevel.D: '🔴'
        }

        print(f"   {quality_emoji.get(quality, '❓')} Качество: {quality.value if quality else 'unknown'}")
        print(f"   📊 Уверенность: {confidence:.3f}")
        print(f"   ⚙️ Метод: {method}")

    def _print_detailed_report(self, results: dict, total_time: float):
        print("\n" + "=" * 60)
        print("📊 ДЕТАЛЬНЫЙ ОТЧЕТ АНАЛИЗА КАЧЕСТВА")
        print("=" * 60)

        successful = [r for r in results.values() if r.get('status') != 'error']
        failed = len(results) - len(successful)

        print(f"\n📋 Общая статистика:")
        print(f"  • Проанализировано файлов: {len(results)}")
        print(f"  • Успешно: {len(successful)}")
        print(f"  • Ошибок: {failed}")
        print(f"  • Время анализа: {total_time:.1f}с")

        print(f"\n✅ Анализ завершен! Файлы готовы к обработке.")
