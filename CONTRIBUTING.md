# 🤝 Руководство по контрибуции

Спасибо за интерес к улучшению проекта! Это руководство поможет вам внести свой вклад правильно.

## 📋 Содержание

- [Кодекс поведения](#кодекс-поведения)
- [Как помочь проекту](#как-помочь-проекту)
- [Процесс разработки](#процесс-разработки)
- [Стандарты кода](#стандарты-кода)
- [Тестирование](#тестирование)
- [Документация](#документация)
- [Pull Request процесс](#pull-request-процесс)

## 📜 Кодекс поведения

- Будьте уважительны к другим участникам
- Конструктивная критика приветствуется
- Токсичное поведение не допускается

## 🎯 Как помочь проекту

### Сообщить о баге

1. Проверьте, что баг еще не reported в Issues
2. Создайте новый Issue с тегом `bug`
3. Опишите:
   - Что вы делали
   - Что ожидали
   - Что произошло на самом деле
   - Версию Python, Django, ОС
   - Шаги для воспроизведения

### Предложить улучшение

1. Создайте Issue с тегом `enhancement`
2. Опишите:
   - Зачем это нужно
   - Как это должно работать
   - Примеры использования

### Исправить баг или добавить feature

1. Найдите открытый Issue или создайте новый
2. Прокомментируйте, что хотите взять задачу
3. Fork репозитория
4. Создайте ветку для изменений
5. Сделайте изменения
6. Создайте Pull Request

## 🔄 Процесс разработки

### 1. Настройка окружения

```bash
# Fork репозитория на GitHub
# Клонируйте ваш fork
git clone https://github.com/YOUR_USERNAME/electronics_network.git
cd electronics_network

# Добавьте upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/electronics_network.git

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows

# Установите зависимости
pip install -r requirements.txt
```

### 2. Создание ветки

```bash
# Обновите main
git checkout main
git pull upstream main

# Создайте feature ветку
git checkout -b feature/your-feature-name
# или
git checkout -b fix/bug-description
```

**Naming convention для веток:**
- `feature/` - новый функционал
- `fix/` - исправление бага
- `docs/` - изменения в документации
- `refactor/` - рефакторинг кода
- `test/` - добавление тестов

### 3. Разработка

Делайте небольшие, логические коммиты:

```bash
git add <files>
git commit -m "Краткое описание изменения"
```

**Формат commit message:**
```
<тип>: <краткое описание>

<детальное описание, если нужно>

Closes #123  # если закрывает Issue
```

**Типы коммитов:**
- `feat:` - новый функционал
- `fix:` - исправление бага
- `docs:` - изменения в документации
- `style:` - форматирование, отсутствующие точки с запятой и т.д.
- `refactor:` - рефакторинг кода
- `test:` - добавление тестов
- `chore:` - обновление задач сборки, конфигов и т.д.

**Примеры:**
```
feat: добавить фильтр по дате создания звена

fix: исправить расчет уровня иерархии при обновлении поставщика

Closes #42

docs: обновить README с примерами фильтрации

test: добавить тесты для валидации поставщика

refactor: оптимизировать запросы в NetworkNodeViewSet
```

## 📏 Стандарты кода

### Python Code Style

Проект следует **PEP 8** с некоторыми адаптациями:

1. **Максимальная длина строки**: 88 символов (black)
2. **Отступы**: 4 пробела
3. **Кавычки**: одинарные для строк, двойные для docstrings
4. **Импорты**: отсортированы с помощью isort

### Обязательные проверки перед коммитом

```bash
# Форматирование кода
black src/

# Сортировка импортов
isort src/

# Проверка PEP8
flake8 src/

# Все проверки должны пройти без ошибок!
```

### Структура кода

```python
"""
Docstring модуля: краткое описание что делает модуль.

Более подробное описание, если необходимо.
"""

# Импорты стандартной библиотеки
import os
from datetime import datetime

# Импорты Django
from django.db import models
from django.contrib.auth import get_user_model

# Импорты сторонних библиотек
from rest_framework import serializers

# Локальные импорты
from .models import NetworkNode


class MyClass:
    """
    Краткое описание класса.
    
    Более детальное описание функциональности класса.
    
    Attributes:
        attr1: Описание атрибута
        attr2: Описание атрибута
    """
    
    def my_method(self, param1: str, param2: int) -> bool:
        """
        Краткое описание метода.
        
        Более подробное описание того, что делает метод.
        
        Args:
            param1: Описание параметра
            param2: Описание параметра
            
        Returns:
            Описание возвращаемого значения
            
        Raises:
            ValueError: Когда возникает эта ошибка
        """
        # Код метода
        pass
```

### Комментарии

- Пишите комментарии на **русском языке**
- Комментируйте **почему**, а не **что**
- Избегайте очевидных комментариев
- Комментируйте сложную бизнес-логику

**Хорошо:**
```python
# Проверяем поставщика, чтобы избежать циклических зависимостей
if self.supplier and self.supplier.id == self.id:
    raise ValidationError("Звено не может быть поставщиком само себе")
```

**Плохо:**
```python
# Присваиваем переменной значение 0
level = 0
```

### Именование

- **Классы**: `CamelCase` (NetworkNode, ProductSerializer)
- **Функции/методы**: `snake_case` (get_full_address, clear_debt)
- **Константы**: `UPPER_SNAKE_CASE` (MAX_LENGTH, DEFAULT_LEVEL)
- **Переменные**: `snake_case`, осмысленные имена

**Хорошо:**
```python
def calculate_hierarchy_level(supplier: NetworkNode) -> int:
    """Рассчитывает уровень иерархии на основе поставщика."""
    if supplier is None:
        return 0
    return supplier.hierarchy_level + 1
```

**Плохо:**
```python
def calc_lvl(s):
    if not s:
        return 0
    return s.hl + 1
```

## 🧪 Тестирование

### Требования к тестам

1. **Каждый новый feature должен иметь тесты**
2. **Каждый fix бага должен иметь тест, воспроизводящий баг**
3. **Тесты должны быть изолированными**
4. **Тесты должны быть быстрыми**

### Запуск тестов

```bash
# Все тесты
pytest

# С покрытием
pytest --cov=network --cov-report=html

# Конкретный файл
pytest tests/unit/test_models.py

# Конкретный тест
pytest tests/unit/test_models.py::TestNetworkNode::test_create_factory
```

### Минимальное покрытие

- **Новый код должен иметь минимум 80% покрытие**
- **Критичные функции - 100% покрытие**

### Структура тестов

```python
import pytest
from network.models import NetworkNode


@pytest.mark.django_db
class TestNetworkNode:
    """Тесты для модели NetworkNode."""
    
    def test_create_factory_node(self):
        """Тест создания завода."""
        # Arrange (подготовка)
        factory_data = {
            'name': 'Test Factory',
            'node_type': NetworkNode.NodeType.FACTORY,
            # ... остальные поля
        }
        
        # Act (действие)
        factory = NetworkNode.objects.create(**factory_data)
        
        # Assert (проверка)
        assert factory.hierarchy_level == 0
        assert factory.supplier is None
```

### Фикстуры

Используйте фикстуры для переиспользуемых данных:

```python
@pytest.fixture
def factory_node(db):
    """Фикстура для создания завода."""
    return NetworkNode.objects.create(
        name='Test Factory',
        node_type=NetworkNode.NodeType.FACTORY,
        # ...
    )


def test_with_fixture(factory_node):
    """Тест использующий фикстуру."""
    assert factory_node.hierarchy_level == 0
```

## 📚 Документация

### Когда обновлять документацию

- Добавление нового API endpoint
- Изменение существующего функционала
- Добавление новых зависимостей
- Изменение процесса установки

### Что документировать

1. **README.md** - общее описание и быстрый старт
2. **API_EXAMPLES.md** - примеры использования API
3. **Docstrings** - все публичные функции, классы, методы
4. **Inline комментарии** - сложная бизнес-логика

### Формат документации

Используйте **Markdown** для всех документов.

**Структура документа:**
```markdown
# Заголовок

Краткое описание.

## Подзаголовок

Детальное описание.

### Примеры

```python
# Пример кода
```

## Примечания

Важные замечания.
```

## 🔄 Pull Request процесс

### Перед созданием PR

1. **Убедитесь, что все тесты проходят**
   ```bash
   pytest
   ```

2. **Проверьте качество кода**
   ```bash
   flake8 src/
   black src/ --check
   isort src/ --check-only
   ```

3. **Обновите документацию** (если нужно)

4. **Добавьте entry в CHANGELOG** (если проект его использует)

### Создание Pull Request

1. **Push изменений в ваш fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Создайте PR на GitHub**
   - Заполните template PR (если есть)
   - Дайте описательное название
   - Опишите что изменилось и зачем
   - Приложите скриншоты (для UI изменений)
   - Укажите связанные Issues

### Template для PR

```markdown
## Описание

Краткое описание изменений.

## Тип изменения

- [ ] Bug fix (исправление бага)
- [ ] New feature (новый функционал)
- [ ] Breaking change (изменение, ломающее обратную совместимость)
- [ ] Documentation update (обновление документации)

## Как протестировано?

Опишите тесты, которые вы добавили или как вручную проверяли.

## Чек-лист

- [ ] Код следует PEP8
- [ ] Добавлены тесты
- [ ] Все тесты проходят
- [ ] Обновлена документация
- [ ] Нет breaking changes (или они документированы)

## Связанные Issues

Closes #123
```

### Review процесс

1. **Maintainer проверит ваш PR**
2. **Могут быть запрошены изменения**
3. **После approve PR будет смержен**

### Что делать если запросили изменения

```bash
# Сделайте изменения
git add <files>
git commit -m "fix: исправление по review"

# Push обновлений
git push origin feature/your-feature-name

# PR обновится автоматически
```

## 🎨 Best Practices

### Django

1. **Используйте Django ORM правильно**
   ```python
   # Хорошо
   nodes = NetworkNode.objects.select_related('supplier')
   
   # Плохо (N+1 проблема)
   nodes = NetworkNode.objects.all()
   for node in nodes:
       print(node.supplier.name)  # Запрос на каждой итерации!
   ```

2. **Валидируйте на уровне модели**
   ```python
   def clean(self):
       if self.node_type == 'FACTORY' and self.supplier:
           raise ValidationError("Завод не может иметь поставщика")
   ```

3. **Используйте transactions для связанных операций**
   ```python
   from django.db import transaction
   
   @transaction.atomic
   def create_node_with_products(node_data, products_data):
       node = NetworkNode.objects.create(**node_data)
       for product_data in products_data:
           Product.objects.create(network_node=node, **product_data)
   ```

### DRF

1. **Разные сериализаторы для разных действий**
   ```python
   def get_serializer_class(self):
       if self.action == 'list':
           return NetworkNodeListSerializer
       return NetworkNodeDetailSerializer
   ```

2. **Оптимизируйте queryset**
   ```python
   def get_queryset(self):
       queryset = super().get_queryset()
       if self.action == 'retrieve':
           queryset = queryset.prefetch_related('products')
       return queryset
   ```

### Безопасность

1. **Никогда не коммитьте секреты**
   - SECRET_KEY
   - Пароли БД
   - API ключи

2. **Используйте .env для чувствительных данных**

3. **Валидируйте входные данные**

4. **Используйте CSRF защиту**

## 📞 Контакты

Если у вас есть вопросы:

1. Создайте Issue с тегом `question`
2. Проверьте существующую документацию
3. Посмотрите закрытые Issues/PRs

## 🙏 Благодарности

Спасибо за вашу помощь в улучшении проекта! Каждый вклад ценен.