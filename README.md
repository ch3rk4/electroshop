# 🏭 Платформа торговой сети электроники

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-10+-blue.svg)](https://www.postgresql.org/)

Онлайн платформа для управления иерархической торговой сетью электроники с REST API и админ-панелью.

## 📋 Содержание

- [Описание проекта](#-описание-проекта)
- [Технологии](#-технологии)
- [Структура проекта](#-структура-проекта)
- [Установка и запуск](#-установка-и-запуск)
- [API документация](#-api-документация)
- [Тестирование](#-тестирование)
- [Особенности реализации](#-особенности-реализации)

## 🎯 Описание проекта

Веб-приложение для управления трехуровневой иерархической структурой торговой сети электроники:

1. **Заводы (уровень 0)** - производители электроники
2. **Розничные сети (уровень 1+)** - крупные торговые сети
3. **Индивидуальные предприниматели (уровень 1+)** - частные продавцы

### Ключевые возможности

✅ Иерархическая структура с автоматическим расчетом уровней  
✅ REST API с полным CRUD функционалом  
✅ Фильтрация по стране, городу и другим параметрам  
✅ Защита поля "Задолженность" от обновления через API  
✅ Удобная админ-панель с массовыми операциями  
✅ Автоматическая документация API (Swagger/ReDoc)  
✅ Полное покрытие тестами  
✅ Соответствие PEP8 и лучшим практикам Django  

## 🛠 Технологии

- **Backend**: Python 3.13, Django 4.2
- **API**: Django REST Framework 3.14
- **БД**: PostgreSQL 10+
- **Документация**: drf-yasg (Swagger/OpenAPI)
- **Тестирование**: pytest, pytest-django, factory-boy
- **Качество кода**: flake8, black, isort

## 📁 Структура проекта

```
electronics_network/
├── src/                              # Исходный код приложения
│   ├── electronics_network/          # Главный Django проект
│   │   ├── __init__.py
│   │   ├── settings.py              # Настройки проекта
│   │   ├── urls.py                  # Главные URL маршруты
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── network/                      # Django приложение
│   │   ├── __init__.py
│   │   ├── models.py                # Модели данных
│   │   ├── admin.py                 # Конфигурация админ-панели
│   │   ├── serializers.py           # DRF сериализаторы
│   │   ├── views.py                 # API представления
│   │   ├── urls.py                  # URL маршруты приложения
│   │   ├── filters.py               # Фильтры для API
│   │   ├── permissions.py           # Права доступа
│   │   └── migrations/              # Миграции БД
│   ├── manage.py                    # Django management
│   └── setup_db.py                  # Скрипт инициализации БД
├── tests/                            # Тесты
│   ├── conftest.py                  # Конфигурация pytest
│   ├── unit/                        # Юнит-тесты
│   │   └── test_models.py
│   └── integration/                 # Интеграционные тесты
│       └── test_api.py
├── .env.example                      # Пример переменных окружения
├── .gitignore                        # Git ignore файл
├── requirements.txt                  # Зависимости Python
├── pytest.ini                        # Конфигурация pytest
├── setup.cfg                         # Конфигурация flake8/isort
└── README.md                         # Документация проекта
```

## 🚀 Установка и запуск

### Предварительные требования

- Python 3.13+
- PostgreSQL 10+
- Git

### Шаг 1: Клонирование репозитория

```bash
git clone <URL_вашего_репозитория>
cd electronics_network
```

### Шаг 2: Создание виртуального окружения

```bash
# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### Шаг 3: Установка зависимостей

```bash
pip install -r requirements.txt
```

### Шаг 4: Настройка базы данных PostgreSQL

```bash
# Войдите в PostgreSQL (команда может отличаться в зависимости от ОС)
psql -U postgres

# Создайте базу данных
CREATE DATABASE electronics_network_db;

# Создайте пользователя (опционально)
CREATE USER electronics_user WITH PASSWORD 'your_password';
ALTER ROLE electronics_user SET client_encoding TO 'utf8';
ALTER ROLE electronics_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE electronics_user SET timezone TO 'Europe/Moscow';
GRANT ALL PRIVILEGES ON DATABASE electronics_network_db TO electronics_user;

# Выйдите из psql
\q
```

### Шаг 5: Настройка переменных окружения

```bash
# Скопируйте файл с примером
cp .env.example .env

# Отредактируйте .env файл, установите свои значения:
# - SECRET_KEY (сгенерируйте новый!)
# - DB_PASSWORD (ваш пароль от PostgreSQL)
# - и другие параметры при необходимости
```

**Генерация SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Шаг 6: Применение миграций

```bash
cd src
python manage.py makemigrations
python manage.py migrate
```

### Шаг 7: Создание тестовых данных

```bash
# Запустите скрипт инициализации БД
python setup_db.py
```

Скрипт создаст:
- Администратора (логин: `admin`, пароль: `admin123`)
- Сотрудника для API (логин: `employee`, пароль: `employee123`)
- Тестовую иерархию торговой сети с заводами, сетями и ИП
- Набор тестовых продуктов

### Шаг 8: Запуск сервера разработки

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: `http://localhost:8000`

### Доступные URL

- **Админ-панель**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/
- **Swagger документация**: http://localhost:8000/swagger/
- **ReDoc документация**: http://localhost:8000/redoc/

## 📚 API документация

### Аутентификация

API требует аутентификации. Поддерживаются следующие методы:

1. **Basic Authentication** - для тестирования в Swagger/Postman
2. **Session Authentication** - для веб-браузера

**Важно**: Доступ к API имеют только **активные сотрудники** (`is_active=True`).

### Основные endpoints

#### Звенья торговой сети

```
GET    /api/network-nodes/              # Список всех звеньев
POST   /api/network-nodes/              # Создать новое звено
GET    /api/network-nodes/{id}/         # Детали звена
PUT    /api/network-nodes/{id}/         # Полное обновление
PATCH  /api/network-nodes/{id}/         # Частичное обновление
DELETE /api/network-nodes/{id}/         # Удалить звено
GET    /api/network-nodes/statistics/   # Статистика по сети
POST   /api/network-nodes/{id}/clear_debt/  # Очистить задолженность
```

#### Продукты

```
GET    /api/products/                   # Список всех продуктов
POST   /api/products/                   # Создать новый продукт
GET    /api/products/{id}/              # Детали продукта
PUT    /api/products/{id}/              # Полное обновление
PATCH  /api/products/{id}/              # Частичное обновление
DELETE /api/products/{id}/              # Удалить продукт
```

### Фильтрация

API поддерживает мощную систему фильтрации:

**Фильтры для звеньев сети:**
```
?country=Россия                         # По стране (точное совпадение)
?city=Москва                           # По городу
?node_type=FACTORY                     # По типу (FACTORY/RETAIL/IE)
?hierarchy_level=1                     # По уровню иерархии
?has_supplier=true                     # С/без поставщика
?has_debt=true                         # С задолженностью
?debt_min=1000&debt_max=100000        # По диапазону долга
```

**Пример запроса:**
```bash
curl -X GET "http://localhost:8000/api/network-nodes/?country=Россия&has_debt=true" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

### Важное ограничение: Поле "debt"

⚠️ **КРИТИЧНО**: Поле `debt` (задолженность) **НЕЛЬЗЯ** изменить через обычные PUT/PATCH запросы!

```json
// ❌ Это вернет ошибку 400
PATCH /api/network-nodes/1/
{
  "debt": "0.00"
}
```

**Правильный способ очистить задолженность:**
```bash
POST /api/network-nodes/1/clear_debt/
```

Или через админ-панель с помощью массового действия.

## 🧪 Тестирование

### Запуск всех тестов

```bash
cd src
pytest
```

### Запуск с покрытием кода

```bash
pytest --cov=network --cov-report=html
```

HTML отчет будет доступен в `htmlcov/index.html`

### Запуск конкретных тестов

```bash
# Только юнит-тесты
pytest tests/unit/

# Только интеграционные тесты
pytest tests/integration/

# Конкретный файл
pytest tests/unit/test_models.py

# Конкретный тест
pytest tests/unit/test_models.py::TestNetworkNodeModel::test_create_factory_node
```

### Проверка качества кода

```bash
# Проверка PEP8 с помощью flake8
flake8 src/

# Форматирование кода с помощью black
black src/

# Сортировка импортов
isort src/
```

## ⚙️ Особенности реализации

### 1. Автоматический расчет уровня иерархии

Уровень иерархии рассчитывается автоматически при сохранении объекта:

```python
def save(self, *args, **kwargs):
    if self.supplier is None:
        self.hierarchy_level = 0  # Завод
    else:
        self.hierarchy_level = self.supplier.hierarchy_level + 1
    super().save(*args, **kwargs)
```

### 2. Защита поля "debt" от обновления

Реализована на уровне сериализатора и view:

```python
# В сериализаторе
read_only_fields = ['id', 'debt']

# В view
def update(self, request, *args, **kwargs):
    if 'debt' in request.data:
        return Response({'error': 'Обновление debt запрещено'}, 
                       status=400)
    return super().update(request, *args, **kwargs)
```

### 3. Оптимизация запросов к БД

Используются `select_related` и `prefetch_related` для предотвращения N+1 проблемы:

```python
def get_queryset(self):
    queryset = super().get_queryset()
    if self.action == 'retrieve':
        queryset = queryset.select_related('supplier')
        queryset = queryset.prefetch_related('products')
    return queryset
```

### 4. Admin Action для массовой очистки долга

```python
@admin.action(description='Очистить задолженность')
def clear_debt(self, request, queryset):
    updated_count = queryset.update(debt=0.00)
    self.message_user(request, f'Очищено {updated_count} записей')
```

### 5. Права доступа

Только активные сотрудники могут работать с API:

```python
class IsActiveEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active
        )
```

## 📝 Модели данных

### NetworkNode (Звено сети)

Представляет узел в торговой сети:

| Поле | Тип | Описание |
|------|-----|----------|
| name | CharField | Название организации |
| node_type | CharField | Тип (FACTORY/RETAIL/IE) |
| email | EmailField | Email |
| country | CharField | Страна |
| city | CharField | Город (с индексом) |
| street | CharField | Улица |
| house_number | CharField | Номер дома |
| supplier | ForeignKey | Поставщик (ссылка на себя) |
| hierarchy_level | PositiveSmallIntegerField | Уровень (0-N) |
| debt | DecimalField | Задолженность |
| created_at | DateTimeField | Дата создания |
| updated_at | DateTimeField | Дата обновления |

### Product (Продукт)

Представляет товар:

| Поле | Тип | Описание |
|------|-----|----------|
| network_node | ForeignKey | Звено сети |
| name | CharField | Название продукта |
| model | CharField | Модель |
| release_date | DateField | Дата выхода на рынок |

## 🤝 Контрибьюция

При внесении изменений, пожалуйста:

1. Следуйте PEP8
2. Добавляйте тесты для нового функционала
3. Обновляйте документацию
4. Проверяйте код с помощью flake8 перед коммитом

## 📄 Лицензия

Этот проект создан в рамках тестового задания.

## 🐛 Известные проблемы / TODO

- [ ] Добавить пагинацию в админ-панели для больших списков
- [ ] Реализовать экспорт данных в Excel/CSV
- [ ] Добавить логирование действий пользователей
- [ ] Реализовать уведомления о задолженностях
- [ ] Добавить графическую визуализацию иерархии

## 📞 Поддержка

При возникновении проблем создайте issue в репозитории.