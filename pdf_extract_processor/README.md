# PDF Extract Processor с RAG модулем

🚀 **Комплексная система обработки PDF документов с поддержкой RAG (Retrieval-Augmented Generation)**

**Автор:** Popov_Andrew  
**Лицензия:** MIT

## ✨ Возможности

- **Продвинутое извлечение текста из PDF** - Высококачественное OCR с несколькими движками
- **Подготовка для RAG систем** - Оптимизировано для векторных баз данных и семантического поиска
- **Умное извлечение метаданных** - Автоматическое определение типов документов, ведомств, дат
- **Чистая обработка текста** - Удаление технических артефактов с сохранением содержания
- **Пакетная обработка** - Эффективная работа с множественными документами
- **Интеграция с Google Colab** - Готовый пайплайн для среды Colab

## 🏗️ Архитектура

```
PDF файлы → ImprovedAdvancedPDFExtractProcessor → RAGProcessor → Векторная БД
```

### Основные компоненты:
- **ImprovedAdvancedPDFExtractProcessor** - Продвинутый движок обработки PDF
- **RAGProcessor** - Специализированный процессор для векторных баз данных
- **UnifiedPDFProcessor** - Универсальное решение для разных сценариев
- **IndependentQualityAnalyzer** - Оценка качества документов

## 🚀 Быстрый старт

### Установка

```bash
git clone https://github.com/Andrew821667/Extract_Processor.git
cd Extract_Processor
pip install -r requirements.txt

# Установка системных зависимостей (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-rus
```

### Базовое использование

```python
from pdf_extract_processor import (
    ImprovedAdvancedPDFExtractProcessor,
    RAGProcessor, 
    UnifiedPDFProcessor
)

# Полный пайплайн: PDF → RAG
unified = UnifiedPDFProcessor()
rag_result = unified.process_file_for_rag("документ.pdf")

# Получение метаданных для векторной БД
print(rag_result['metadata'])
# {'ministry': 'Минздрав РФ', 'date': '2025-06-05', 'doc_number': '123'}

# Получение чистого текста для векторизации
print(f"Чистый текст: {rag_result['chars']} символов")
print(f"Эффективность: {rag_result['processing_info']['content_ratio']:.1f}%")
```

### Обработка готового вывода

```python
from pdf_extract_processor import quick_rag_from_output

# Если у вас уже есть вывод процессора
result = quick_rag_from_output(processor_output)
```

### Пайплайн для Google Colab

```python
from pdf_extract_processor.rag.integration import colab_rag_pipeline

# Полный пайплайн с загрузкой и скачиванием файлов
colab_rag_pipeline()
```

## 📊 Формат вывода

### Структура метаданных
```yaml
filename: "документ.pdf"
title: "Приказ Министерства здравоохранения РФ"
document_type: "приказ"
ministry: "Минздрав РФ"  
date: "2025-06-05"
doc_number: "123"
status: "действующий"
```

### Результат обработки
```python
{
    'metadata': {...},              # YAML метаданные выше
    'text': 'Чистый текст документа...',  # Готов для векторизации
    'chars': 15000,                # Количество символов
    'processing_info': {
        'original_size': 18000,
        'content_ratio': 83.3,     # Процент эффективности
        'processing_date': '2025-06-05T14:30:00'
    }
}
```

### Markdown готовый для RAG
```markdown
---
filename: "документ.pdf"
ministry: "Минздрав РФ"
date: "2025-06-05"
---

МИНИСТЕРСТВО ЗДРАВООХРАНЕНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ

ПРИКАЗ
от 5 июня 2025 г. № 123

О внедрении новых технологий...
```

## 🗄️ Интеграция с векторными базами данных

### ChromaDB
```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("legal_documents")

# Добавление обработанного документа
collection.add(
    documents=[rag_result['text']],
    metadatas=[rag_result['metadata']],
    ids=[rag_result['metadata']['filename']]
)

# Запрос с фильтрами
results = collection.query(
    query_texts=["требования к медицинскому оборудованию"],
    where={"ministry": "Минздрав РФ"},
    n_results=5
)
```

### Pinecone
```python
import pinecone
from openai import OpenAI

# Получение эмбеддингов
client = OpenAI()
embeddings = client.embeddings.create(
    input=rag_result['text'],
    model="text-embedding-ada-002"
)

# Загрузка в Pinecone
index.upsert([
    (
        rag_result['metadata']['filename'],
        embeddings.data[0].embedding,
        rag_result['metadata']
    )
])
```

### Weaviate
```python
import weaviate

client = weaviate.Client("http://localhost:8080")

# Создание схемы
schema = {
    "class": "LegalDocument",
    "properties": [
        {"name": "content", "dataType": ["text"]},
        {"name": "ministry", "dataType": ["string"]},
        {"name": "date", "dataType": ["string"]},
        {"name": "docNumber", "dataType": ["string"]}
    ]
}

# Добавление документа
client.data_object.create(
    data_object={
        "content": rag_result['text'],
        **rag_result['metadata']
    },
    class_name="LegalDocument"
)
```

## 📱 Использование в Google Colab

### Простой запуск
```python
# Установка в новой ячейке
!git clone https://github.com/Andrew821667/Extract_Processor.git
%cd Extract_Processor
!pip install -r requirements.txt --quiet
!apt-get install tesseract-ocr tesseract-ocr-rus --quiet

# Использование
from pdf_extract_processor.rag.integration import colab_rag_pipeline
colab_rag_pipeline()
```

### Пошаговая обработка
```python
from pdf_extract_processor import UnifiedPDFProcessor
from google.colab import files

# Загрузка файлов
uploaded = files.upload()

# Обработка
processor = UnifiedPDFProcessor()
for filename in uploaded.keys():
    if filename.endswith('.pdf'):
        result = processor.process_file_for_rag(filename)
        print(f"✅ {filename}: {result['chars']} символов")
```

## 🔧 Продвинутое использование

### Пакетная обработка
```python
import os
from pathlib import Path

processor = UnifiedPDFProcessor()
pdf_files = list(Path("./documents").glob("*.pdf"))

results = []
for pdf_file in pdf_files:
    try:
        result = processor.process_file_for_rag(str(pdf_file))
        results.append(result)
        print(f"✅ {pdf_file.name}: {result['chars']} символов")
    except Exception as e:
        print(f"❌ {pdf_file.name}: {e}")

print(f"\n📊 Обработано: {len(results)} из {len(pdf_files)} файлов")
```

### Настройка RAG процессора
```python
from pdf_extract_processor.rag.rag_processor import RAGProcessor

# Создание кастомного процессора
rag = RAGProcessor()

# Добавление новых паттернов ведомств
rag.metadata_extractors['ministry_patterns']['НОВОЕ ВЕДОМСТВО'] = 'Новое ведомство РФ'

# Обработка
result = rag.process_single_document(processor_output)
```

### Создание чанков для векторизации
```python
def create_chunks(text, chunk_size=1000, overlap=100):
    """Разбивка текста на чанки для векторизации."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks

# Использование
chunks = create_chunks(rag_result['text'])
print(f"Создано чанков: {len(chunks)}")
```

## 📋 Поддерживаемые типы документов

- **Приказы министерств** - автоматическое определение ведомства
- **Постановления правительства** - извлечение номеров и дат
- **Указы президента** - структурирование содержания
- **Технические регламенты** - сохранение нумерации пунктов
- **Методические рекомендации** - очистка от служебной информации

## 🎯 Метрики качества

Система автоматически отслеживает:
- **Эффективность извлечения** - процент сохраненного контента (цель: 80-90%)
- **Качество OCR** - уверенность распознавания текста
- **Полнота метаданных** - количество извлеченных атрибутов
- **Скорость обработки** - время на документ

## 🛠️ Требования

### Python пакеты
```
PyMuPDF>=1.23.0
pdfplumber>=0.9.0
pytesseract>=0.3.10
easyocr>=1.7.0
opencv-python>=4.8.0
Pillow>=10.0.0
numpy>=1.24.0
pandas>=2.0.0
spacy>=3.6.0
nltk>=3.8.1
markdown>=3.4.0
PyYAML>=6.0.1
```

### Системные зависимости
- Tesseract OCR
- Языковые пакеты Tesseract (русский)

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Запушьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 📞 Поддержка

- **GitHub Issues** - для багов и предложений функций
- **Документация** - в директории `docs/`
- **Примеры** - в директории `examples/`

## 🏆 Благодарности

- Команде Tesseract за отличное OCR решение
- Разработчикам PyMuPDF за работу с PDF
- Сообществу за тестирование и обратную связь

---

**Автор:** Popov_Andrew  
**Версия:** 2.1.0  
**Лицензия:** MIT
