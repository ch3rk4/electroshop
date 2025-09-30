# ⚡ Quick Start Guide

Быстрый старт для запуска проекта после клонирования репозитория.

## 📦 Предварительные требования

- Python 3.13+
- PostgreSQL 10+
- Git

## 🚀 Запуск за 5 минут

### 1. Клонирование и подготовка

```bash
# Клонируйте репозиторий
git clone <URL_репозитория>
cd electronics_network

# Создайте и активируйте виртуальное окружение
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

### 2. Настройка базы данных

```bash
# Войдите в PostgreSQL
psql -U postgres

# Создайте базу данных
CREATE DATABASE electronics_network_db;
CREATE USER electronics_user WITH PASSWORD 'YourPassword123';
GRANT ALL PRIVILEGES ON DATABASE electronics_network_db TO electronics_user;
\q
```

### 3. Настройка окружения

```bash
# Скопируйте пример конфигурации
cp .env.example .env

# Сгенерируйте SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Отредактируйте .env файл:
# - Вставьте сгенерированный SECRET_KEY
# - Укажите пароль для БД (DB_PASSWORD)
```

### 4. Применение миграций и инициализация

```bash
cd src

# Примените миграции
python manage.py migrate

# Создайте тестовые данные
python setup_db.py
```

### 5. Запуск сервера

```bash
# Запустите сервер разработки
python manage.py runserver
```

## 🎉 Готово!

Откройте в браузере:

- **Админ-панель**: http://localhost:8000/admin/
  - Логин: `admin`
  - Пароль: `admin123`

- **API Swagger**: http://localhost:8000/swagger/
  - Для API используйте: `employee` / `employee123`

- **API Endpoints**: http://localhost:8000/api/

## 🧪 Запуск тестов

```bash
# В директории src
pytest

# С покрытием
pytest --cov=network
```

## 📚 Дополнительная документация

- [README.md](README.md) - Полная документация проекта
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Подробное руководство по развертыванию
- [API_EXAMPLES.md](API_EXAMPLES.md) - Примеры API запросов

## 🐛 Проблемы?

Если что-то не работает, см. раздел "Решение проблем" в [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)