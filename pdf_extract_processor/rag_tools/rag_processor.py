"""
RAG Tools для Extract_Processor
Инструменты для подготовки данных для RAG-систем
"""

import re
import os
from datetime import datetime
from typing import List, Dict, Any

def clean_npa_for_rag(text: str, document_title: str = "") -> str:
    """
    🧹 ИДЕАЛЬНАЯ ОЧИСТКА НПА ДЛЯ RAG-СИСТЕМЫ
    Убираем ВСЮ служебную информацию, оставляем только содержание
    """
    
    # 1. Убираем ВСЮ служебную информацию системы обработки
    text = re.sub(r'# Извлеченный текст.*?---', '', text, flags=re.DOTALL)
    text = re.sub(r'\*\*Файл:\*\*.*?\n', '', text)
    text = re.sub(r'\*\*Качество:\*\*.*?\n', '', text)
    text = re.sub(r'\*\*Метод:\*\*.*?\n', '', text)
    text = re.sub(r'\*\*Уверенность:\*\*.*?\n', '', text)
    
    # 2. Убираем разделители страниц и служебные коды
    text = re.sub(r'--- Страница \d+ ---\n*', '', text)
    text = re.sub(r'=== Страница \d+ ===\n*', '', text)
    
    # 3. Убираем OCR артефакты
    text = re.sub(r'\n[А-Я]{1,3}\s*\n', '\n', text)
    text = re.sub(r'\n[^\w\s]{1,3}\n', '\n', text)
    
    # 4. Улучшаем структуру для RAG
    lines = text.split('\n')
    clean_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Главные заголовки органов власти
        if re.match(r'(ПРАВИТЕЛЬСТВО|МИНИСТЕРСТВО|ФЕДЕРАЛЬНАЯ СЛУЖБА)', line):
            clean_lines.append(f'# {line}')
            continue

        # Тип документа
        if line in ['ПОСТАНОВЛЕНИЕ', 'ПРИКАЗ', 'РАСПОРЯЖЕНИЕ', 'УКАЗ', 'РЕШЕНИЕ']:
            clean_lines.append(f'## {line}')
            continue

        # Основные пункты
        if re.match(r'^\d+\.\s+[А-ЯЁ]', line):
            clean_lines.append(f'### {line}')
            continue

        # Обычный текст
        clean_lines.append(line)

    # 5. Финальная очистка
    result = '\n\n'.join([line for line in clean_lines if line.strip()])
    result = re.sub(r' +', ' ', result)
    result = re.sub(r'\n{3,}', '\n\n', result)

    return result.strip()

class RAGDataProcessor:
    """Процессор для подготовки данных для RAG"""
    
    def __init__(self):
        self.processed_docs = []
        
    def process_multiple_npa(self, pdf_files: List[str]) -> str:
        """Обработка нескольких НПА в один файл для RAG"""
        
        all_documents = []
        
        for pdf_file in pdf_files:
            try:
                # Здесь должна быть логика извлечения из PDF
                # Пока заглушка
                clean_text = f"Обработанный документ: {pdf_file}"
                
                all_documents.append({
                    'filename': pdf_file,
                    'content': clean_text,
                    'size': len(clean_text)
                })
                
            except Exception as e:
                print(f"Ошибка с {pdf_file}: {e}")
        
        # Объединяем документы
        if all_documents:
            combined_content = ["# СБОРНИК НОРМАТИВНО-ПРАВОВЫХ АКТОВ", ""]
            
            for i, doc in enumerate(all_documents, 1):
                combined_content.append(f"## Документ {i}: {doc['filename']}")
                combined_content.append("")
                combined_content.append(doc['content'])
                combined_content.append("")
                combined_content.append("---")
                combined_content.append("")
            
            return '\n'.join(combined_content)
        
        return ""
