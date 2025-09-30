"""
URL маршруты для приложения network.

Этот модуль определяет маршруты API для работы с торговой сетью.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import NetworkNodeViewSet, ProductViewSet

# Создаем роутер для автоматической генерации URL
# DefaultRouter создает стандартные URL для всех CRUD операций
router = DefaultRouter()

# Регистрируем ViewSets в роутере
# Первый аргумент - префикс URL, второй - ViewSet, третий - basename
router.register(r'network-nodes', NetworkNodeViewSet, basename='networknode')
router.register(r'products', ProductViewSet, basename='product')

# URL паттерны приложения
app_name = 'network'

urlpatterns = [
    # Включаем все URL, сгенерированные роутером
    # Это создаст endpoints:
    # - /api/network-nodes/
    # - /api/network-nodes/{id}/
    # - /api/network-nodes/statistics/
    # - /api/network-nodes/{id}/clear_debt/
    # - /api/products/
    # - /api/products/{id}/
    path('', include(router.urls)),
]