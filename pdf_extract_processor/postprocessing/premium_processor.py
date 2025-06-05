"""
Улучшенная постобработка для Extract_Processor
Основан на коде из исследовательского ноутбука
"""

import re
from datetime import datetime
from typing import Dict, Any, List

def process_any_text_to_premium_fixed(text: str) -> str:
    """
    🔧 ИСПРАВЛЕННАЯ постобработка без порчи текста
    """
    
    if not text or len(text.strip()) < 10:
        return "# Ошибка\n\nТекст слишком короткий"

    # БЕЗОПАСНЫЕ исправления (только очевидные OCR ошибки)
    safe_fixes = {
        'соответствипунктом': 'соответствии с пунктом',
        'лицензированиотдельных': 'лицензировании отдельных',
        'фармацевтической': 'фармацевтической',
        'нформация документе': 'Информация о документе',
        'пнадзору': 'по надзору',
        'ЗДРАВООХРАНЕНЯ': 'ЗДРАВООХРАНЕНИЯ',
        'СТРАНЦА': 'СТРАНИЦА',
    }

    # Применяем ТОЛЬКО безопасные исправления
    for error, fix in safe_fixes.items():
        if error in text:
            text = text.replace(error, fix)

    # Безопасное улучшение структуры
    lines = text.split('\n')
    improved_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            improved_lines.append('')
            continue

        # НЕ ТРОГАЕМ уже хорошие заголовки
        if line.startswith('#'):
            improved_lines.append(line)
            continue

        # Простое улучшение абзацев
        if len(line) > 100 and line.endswith('.'):
            improved_lines.append(line)
            improved_lines.append('')  # Добавляем перенос
        else:
            improved_lines.append(line)

    result = '\n'.join(improved_lines)
    
    # Безопасная очистка множественных переносов
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    # Добавляем метку обработки
    result += f'\n\n---\n\n*Документ обработан улучшенной системой {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*'
    
    return result

class PremiumPostProcessor:
    """Премиум класс постобработки"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
    def process(self, text: str) -> str:
        """Обработка текста"""
        return process_any_text_to_premium_fixed(text)
        
    def batch_process(self, texts: List[str]) -> List[str]:
        """Пакетная обработка"""
        return [self.process(text) for text in texts]
