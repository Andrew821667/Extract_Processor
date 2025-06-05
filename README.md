# PDF Extract Processor 📄🔍

Продвинутая система извлечения и обработки текста из PDF документов с поддержкой таблиц, OCR и интеллектуального форматирования.

## 🎯 Основные возможности

- **🔍 Интеллектуальный анализ качества PDF**
- **📊 Гибридное извлечение контента** 
- **🧠 Продвинутое OCR** - Tesseract + EasyOCR
- **📋 Обработка таблиц**
- **⚖️ Специализация для нормативных документов**
- **📝 Markdown форматирование**

## 🚀 Быстрый старт

```python
from pdf_extract_processor import AdvancedPDFExtractProcessor

processor = AdvancedPDFExtractProcessor()
results = processor.interactive_process_advanced()
```

## 📦 Установка

```bash
pip install -r requirements.txt
```

## 🔧 Технологии

- PyMuPDF, pdfplumber
- Tesseract OCR, EasyOCR
- OpenCV, spaCy, NLTK

## 📄 Лицензия

MIT License


## 🚀 Новые возможности v2.0

### ✨ Премиум постобработка
- Безопасное исправление OCR ошибок
- Улучшение структуры документа  
- Сохранение исходного форматирования

### 🤖 RAG-инструменты
- Очистка НПА от служебной информации
- Подготовка для векторизации
- Объединение нескольких документов

### 📦 Новые модули
- `postprocessing.premium_processor` - Премиум постобработка
- `rag_tools.rag_processor` - RAG инструменты
- Обновленная конфигурация

### 🔧 Использование

```python
from pdf_extract_processor import AdvancedPDFExtractProcessor
from pdf_extract_processor.postprocessing.premium_processor import PremiumPostProcessor

# Извлечение + постобработка
processor = AdvancedPDFExtractProcessor()
postprocessor = PremiumPostProcessor()

result = processor.process_single_file_advanced("document.pdf")
enhanced = postprocessor.process(str(result))
```

Обновлено: 2025-06-05