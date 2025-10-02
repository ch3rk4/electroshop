# 🚀 Полное руководство по развертыванию проекта

Это подробное пошаговое руководство для развертывания проекта с нуля в терминале PyCharm.

## 📋 Предварительная подготовка

### 1. Установка необходимого ПО

Убедитесь, что у вас установлено:

- **Python 3.13** - [Скачать](https://www.python.org/downloads/)
- **PostgreSQL 10+** - [Скачать](https://www.postgresql.org/download/)
- **Git** - [Скачать](https://git-scm.com/downloads/)
- **PyCharm** - любая версия

## 🎬 Пошаговая инструкция

### Этап 1: Создание структуры проекта

Откройте терминал в PyCharm (Alt+F12) и выполните следующие команды:

```bash
# 1. Создайте директорию проекта
mkdir electronics_network
cd electronics_network

# 2. Инициализируйте Git репозиторий
git init

# 3. Создайте структуру директорий
mkdir -p src/electronics_network src/network tests/unit tests/integration config docs

# 4. Создайте __init__.py файлы
# Windows PowerShell:
New-Item -ItemType File -Path "src\__init__.py"
New-Item -ItemType File -Path "src\network\__init__.py"
New-Item -ItemType File -Path "tests\__init__.py"
New-Item -ItemType File -Path "tests\unit\__init__.py"
New-Item -ItemType File -Path "tests\integration\__init__.py"

# Linux/Mac:
touch src/__init__.py
touch src/network/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
```

### Этап 2: Создание виртуального окружения

```bash
# 1. Создайте виртуальное окружение
python -m venv venv

# 2. Активируйте виртуальное окружение
# Windows CMD:
venv\Scripts\activate.bat

# Windows PowerShell:
venv\Scripts\Activate.ps1

# Linux/Mac:
source venv/bin/activate

# После активации вы должны увидеть (venv) в начале строки терминала
```

### Этап 3: Создание файлов конфигурации

#### 3.1 Создайте requirements.txt

```bash
# Windows:
notepad requirements.txt

# Linux/Mac:
nano requirements.txt
```

Вставьте содержимое из артефакта "requirements.txt" и сохраните (Ctrl+S, затем закройте).

#### 3.2 Создайте .env.example

```bash
# Windows:
notepad .env.example

# Linux/Mac:
nano .env.example
```

Вставьте содержимое из артефакта ".env.example" и сохраните.

#### 3.3 Создайте .gitignore

```bash
# Windows:
notepad .gitignore

# Linux/Mac:
nano .gitignore
```

Вставьте содержимое из артефакта ".gitignore" и сохраните.

#### 3.4 Создайте setup.cfg

```bash
# Windows:
notepad setup.cfg

# Linux/Mac:
nano setup.cfg
```

Вставьте содержимое из артефакта "setup.cfg" и сохраните.

#### 3.5 Создайте pytest.ini

```bash
# Windows:
notepad pytest.ini

# Linux/Mac:
nano pytest.ini
```

Вставьте содержимое из артефакта "pytest.ini" и сохраните.

### Этап 4: Установка зависимостей

```bash
# Обновите pip до последней версии
python -m pip install --upgrade pip

# Установите все зависимости
pip install -r requirements.txt

# Это займет несколько минут. Дождитесь завершения установки.
```

### Этап 5: Настройка PostgreSQL

```bash
# 1. Откройте PostgreSQL командную строку
# Windows: Найдите "SQL Shell (psql)" в меню Пуск
# Linux/Mac: выполните команду
psql -U postgres

# 2. В psql выполните следующие команды:
CREATE DATABASE electronics_network_db;
CREATE USER electronics_user WITH PASSWORD 'SecurePassword123!';
ALTER ROLE electronics_user SET client_encoding TO 'utf8';
ALTER ROLE electronics_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE electronics_user SET timezone TO 'Europe/Moscow';
GRANT ALL PRIVILEGES ON DATABASE electronics_network_db TO electronics_user;

# 3. Выйдите из psql
\q
```

### Этап 6: Создание Django проекта

```bash
# 1. Перейдите в директорию src
cd src

# 2. Создайте Django проект
django-admin startproject electronics_network .

# 3. Создайте Django приложение
python manage.py startapp network

# 4. Вернитесь в корневую директорию
cd ..
```

### Этап 7: Создание файлов приложения

Теперь вам нужно создать файлы с кодом. Используйте PyCharm для удобства:

#### 7.1 Файлы в src/electronics_network/

1. **src/electronics_network/settings.py** - замените содержимое файла на код из артефакта
2. **src/electronics_network/urls.py** - замените содержимое файла на код из артефакта

#### 7.2 Файлы в src/network/

1. **src/network/models.py** - замените содержимое файла
2. **src/network/admin.py** - замените содержимое файла
3. **src/network/serializers.py** - создайте новый файл
4. **src/network/views.py** - замените содержимое файла
5. **src/network/urls.py** - создайте новый файл
6. **src/network/filters.py** - создайте новый файл
7. **src/network/permissions.py** - создайте новый файл

#### 7.3 Вспомогательные файлы

1. **src/setup_db.py** - создайте файл со скриптом инициализации

#### 7.4 Файлы тестов

1. **tests/conftest.py** - создайте файл с фикстурами
2. **tests/unit/test_models.py** - создайте файл с юнит-тестами
3. **tests/integration/test_api.py** - создайте файл с интеграционными тестами

**Совет**: В PyCharm используйте Ctrl+N для быстрого создания новых файлов в выбранной директории.

### Этап 8: Настройка переменных окружения

```bash
# 1. Скопируйте пример файла окружения
cp .env.example .env

# 2. Сгенерируйте SECRET_KEY для Django
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 3. Откройте .env для редактирования
# Windows:
notepad .env

# Linux/Mac:
nano .env

# 4. Замените значения:
#    - SECRET_KEY на сгенерированный ключ
#    - DB_PASSWORD на ваш пароль от PostgreSQL
#    - При необходимости измените другие параметры

# 5. Сохраните файл
```

### Этап 9: Применение миграций

```bash
# 1. Перейдите в директорию src
cd src

# 2. Создайте миграции для приложения network
python manage.py makemigrations network

# Вы должны увидеть сообщение о создании миграций

# 3. Примените все миграции
python manage.py migrate

# Должны создаться все таблицы в БД

# 4. Вернитесь в корень проекта
cd ..
```

### Этап 10: Инициализация базы данных тестовыми данными

```bash
# 1. Перейдите в src
cd src

# 2. Запустите скрипт инициализации
python setup_db.py

# Скрипт создаст:
# - Администратора (admin / admin123)
# - Сотрудника (employee / employee123)
# - Тестовую иерархию сети
# - Набор продуктов

# 3. Вернитесь в корень
cd ..
```

### Этап 11: Запуск сервера разработки

```bash
# 1. Перейдите в src
cd src

# 2. Запустите сервер
python manage.py runserver

# Вы должны увидеть:
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CTRL