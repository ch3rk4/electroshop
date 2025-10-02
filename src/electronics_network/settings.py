"""
Django настройки для проекта electronics_network.

Этот модуль содержит все конфигурации Django, включая настройки БД,
middleware, приложений, статических файлов и безопасности.
"""

import os
import importlib
import importlib.util

from pathlib import Path

from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
# Это позволяет хранить чувствительные данные отдельно от кода
if os.name == "nt":
    for locale_var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        os.environ.setdefault(locale_var, "C")

load_dotenv(encoding="utf-8-sig")

# На Windows при работе с PostgreSQL через psycopg2 может возникать ошибка
# UnicodeDecodeError, если переменные окружения с учетными данными содержат
# символы вне ASCII, а клиентская кодировка не задана. Явно указываем
# PostgreSQL, что клиент ожидает UTF-8, чтобы libpq корректно обрабатывал
# такие значения и сообщения об ошибках.
os.environ.setdefault("PGCLIENTENCODING", "UTF8")


def _normalize_env_value(value: str) -> str:
    """Удаляет невидимые символы, которые часто появляются при копировании."""

    # Стандартные методы вроде str.strip() не всегда убирают zero-width
    # символы или BOM. Они часто встречаются в .env файлах, которые редактируют
    # в текстовых редакторах Windows.
    junk_chars = {"\ufeff", "\u200b", "\u200e", "\u200f", "\u00a0"}
    for junk in junk_chars:
        value = value.replace(junk, "")
    return value.strip()


def get_env_setting(name: str, default: str = "") -> str:
    """Возвращает очищенное строковое значение переменной окружения."""

    raw_value = os.getenv(name, default)
    return _normalize_env_value(raw_value if raw_value is not None else default)

# Определяем базовую директорию проекта
# Path(__file__).resolve() получает полный путь к текущему файлу
# .parent.parent поднимается на две директории вверх (к src/)
BASE_DIR = Path(__file__).resolve().parent.parent

# СЕКЦИЯ БЕЗОПАСНОСТИ
# ===================

# Секретный ключ Django - используется для криптографических операций
# ВАЖНО: В продакшене НИКОГДА не храните ключ в коде!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key-change-in-production')

# Режим отладки - в продакшене ВСЕГДА должен быть False
# При DEBUG=True Django показывает подробные ошибки, что небезопасно в проде
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Список хостов, с которых разрешены запросы
# В продакшене укажите только реальные домены вашего сайта
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# ПРИЛОЖЕНИЯ
# ==========

# Django приложения, которые мы используем в проекте
INSTALLED_APPS = [
    # Встроенные Django приложения - обеспечивают основной функционал
    'django.contrib.admin',  # Админ-панель
    'django.contrib.auth',  # Система аутентификации
    'django.contrib.contenttypes',  # Система типов контента
    'django.contrib.sessions',  # Управление сессиями
    'django.contrib.messages',  # Фреймворк сообщений
    'django.contrib.staticfiles',  # Управление статическими файлами

    # Сторонние приложения - расширяют функционал Django
    'rest_framework',  # Django REST Framework для создания API
    'django_filters',  # Фильтрация данных в API
    'drf_yasg',  # Автоматическая генерация API документации (Swagger)

    # Наши приложения - основная бизнес-логика
    'network',  # Приложение для управления торговой сетью
]

# MIDDLEWARE
# ==========

# Middleware обрабатывают запросы и ответы на разных этапах
# Порядок важен! Каждый middleware вызывается сверху вниз при запросе
# и снизу вверх при ответе
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Добавляет защиту
    'django.contrib.sessions.middleware.SessionMiddleware',  # Управляет сессиями
    'django.middleware.common.CommonMiddleware',  # Общие функции
    'django.middleware.csrf.CsrfViewMiddleware',  # Защита от CSRF атак
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Аутентификация
    'django.contrib.messages.middleware.MessageMiddleware',  # Сообщения
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Защита от clickjacking
]

# Корневой URLconf - точка входа для всех URL маршрутов
ROOT_URLCONF = 'electronics_network.urls'

# ШАБЛОНЫ
# ========

# Настройки для Django шаблонизатора
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Директория с шаблонами
        'APP_DIRS': True,  # Искать шаблоны в директориях приложений
        'OPTIONS': {
            'context_processors': [
                # Процессоры контекста - добавляют переменные во все шаблоны
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI приложение для production сервера
WSGI_APPLICATION = 'electronics_network.wsgi.application'


# БАЗА ДАННЫХ
# ============

# Настройки подключения к PostgreSQL
# Используем переменные окружения для гибкости и безопасности
_db_engine = get_env_setting('DB_ENGINE', 'django.db.backends.postgresql')
_db_options = {}

if _db_engine.endswith('postgresql'):
    # Обеспечиваем использование UTF-8 даже если сервер настроен иначе и
    # принудительно переключаем локаль сообщений на "C", чтобы libpq
    # возвращал ASCII-сообщения. На Windows PostgreSQL по умолчанию может
    # использовать локаль `Russian_Russia.1251`, и при попытке декодировать
    # сообщения об ошибках в UTF-8 psycopg2 выбрасывает UnicodeDecodeError.
    # Передавая lc_messages=C, мы получаем только ASCII-символы и избегаем
    # подобных сбоев, даже когда соединение не удается установить.
    forced_options = "-c client_encoding=UTF8 -c lc_messages=C"

    existing_options = os.getenv('PGOPTIONS', '').strip()
    if existing_options:
        forced_options = f"{existing_options} {forced_options}"

    _db_options['options'] = forced_options

DATABASES = {
    'default': {
        'ENGINE': _db_engine,
        'NAME': get_env_setting('DB_NAME', 'electronics_network_db'),
        'USER': get_env_setting('DB_USER', 'postgres'),
        'PASSWORD': get_env_setting('DB_PASSWORD', ''),
        'HOST': get_env_setting('DB_HOST', 'localhost'),
        'PORT': get_env_setting('DB_PORT', '5432'),
        'OPTIONS': _db_options,
    }
}


# ВАЛИДАЦИЯ ПАРОЛЕЙ
# =================

# Валидаторы обеспечивают безопасность паролей пользователей
AUTH_PASSWORD_VALIDATORS = [
    {
        # Проверяет, что пароль не похож на атрибуты пользователя
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Минимальная длина пароля (по умолчанию 8 символов)
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Проверяет пароль по списку распространенных паролей
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Проверяет, что пароль не состоит только из цифр
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ИНТЕРНАЦИОНАЛИЗАЦИЯ
# ===================

# Настройки языка и времени
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'ru-ru')  # Русский язык по умолчанию
TIME_ZONE = os.getenv('TIME_ZONE', 'Europe/Moscow')  # Московское время
USE_I18N = True  # Включаем интернационализацию
USE_TZ = True  # Используем timezone-aware datetime объекты


# СТАТИЧЕСКИЕ ФАЙЛЫ
# ==================

# URL для доступа к статическим файлам (CSS, JavaScript, изображения)
STATIC_URL = 'static/'
# Директория для сбора всех статических файлов при деплое
STATIC_ROOT = BASE_DIR / 'staticfiles'

# MEDIA ФАЙЛЫ
# ===========

# URL и директория для загружаемых пользователями файлов
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# НАСТРОЙКИ ПЕРВИЧНОГО КЛЮЧА
# ===========================

# Тип поля по умолчанию для автоматических первичных ключей
# BigAutoField позволяет хранить большие целые числа (до 9 квинтиллионов)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# НАСТРОЙКИ DJANGO REST FRAMEWORK
# ================================

REST_FRAMEWORK = {
    # Классы аутентификации - определяют как идентифицируем пользователя
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # BasicAuthentication - простая аутентификация через HTTP заголовки
        'rest_framework.authentication.BasicAuthentication',
        # SessionAuthentication - использует Django сессии
        'rest_framework.authentication.SessionAuthentication',
    ],

    # Классы прав доступа по умолчанию
    # IsAuthenticated требует, чтобы пользователь был авторизован
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    # Пагинация - разбиваем большие списки на страницы
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,  # 20 объектов на страницу

    # Фильтрация - позволяет фильтровать результаты API
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],

    # Формат datetime в API ответах (ISO 8601 формат)
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
}


# НАСТРОЙКИ SWAGGER (API ДОКУМЕНТАЦИЯ)
# =====================================

SWAGGER_SETTINGS = {
    # Методы аутентификации для Swagger UI
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
    },
    # Использовать только эти методы аутентификации
    'USE_SESSION_AUTH': True,
    'LOGIN_URL': '/admin/login/',
    'LOGOUT_URL': '/admin/logout/',
}