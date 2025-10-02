"""
Главные URL маршруты проекта electronics_network.

Этот модуль является точкой входа для всех URL маршрутов проекта.
Здесь мы подключаем админ-панель, API endpoints и документацию Swagger.
"""

from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Настройка Swagger/OpenAPI документации
schema_view = get_schema_view(
    openapi.Info(
        title="Electronics Network API",
        default_version='v1',
        description="""
        API для управления торговой сетью электроники.
        
        ## Описание
        Этот API предоставляет возможность управления иерархической структурой 
        торговой сети электроники, включающей заводы, розничные сети и 
        индивидуальных предпринимателей.
        
        ## Основные возможности:
        - CRUD операции для звеньев торговой сети
        - CRUD операции для продуктов
        - Фильтрация по стране, городу и другим параметрам
        - Получение статистики по всей сети
        - Управление иерархией поставщиков
        
        ## Аутентификация
        Для доступа к API необходимо быть аутентифицированным активным сотрудником.
        API поддерживает Basic Authentication и Session Authentication.
        
        ## Важные ограничения:
        - Поле 'debt' (задолженность) **НЕЛЬЗЯ** обновить через обычные PUT/PATCH запросы
        - Для очистки задолженности используйте специальный endpoint: POST /api/network-nodes/{id}/clear_debt/
        """,
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@electronicsnetwork.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],  # Документация доступна всем
)

urlpatterns = [
    # Админ-панель Django
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include('network.urls', namespace='network')),

    # Swagger UI - интерактивная документация API
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),

    # ReDoc - альтернативный интерфейс документации
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),

    # JSON схема API
    path(
        'swagger.json',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),

    # DRF browsable API authentication URLs
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Настройка заголовка админ-панели
admin.site.site_header = "Управление торговой сетью электроники"
admin.site.site_title = "Админ-панель Electronics Network"
admin.site.index_title = "Добро пожаловать в панель управления"