"""
API представления для торговой сети.

Этот модуль содержит ViewSets для обработки CRUD операций
через REST API с использованием Django REST Framework.
"""

from django.db.models import Avg, Count, Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import NetworkNodeFilter, ProductFilter
from .models import NetworkNode, Product
from .permissions import IsActiveEmployee
from .serializers import (
    NetworkNodeCreateUpdateSerializer,
    NetworkNodeDetailSerializer,
    NetworkNodeListSerializer,
    NetworkNodeStatisticsSerializer,
    ProductSerializer,
)


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления звеньями торговой сети.

    Предоставляет CRUD операции (Create, Read, Update, Delete) для звеньев сети.

    ВАЖНО: Согласно ТЗ, поле 'debt' (задолженность) ЗАПРЕЩЕНО обновлять через API.
    Это контролируется через сериализатор NetworkNodeCreateUpdateSerializer.

    Endpoints:
        GET    /api/network-nodes/          - Список всех звеньев
        POST   /api/network-nodes/          - Создать новое звено
        GET    /api/network-nodes/{id}/     - Детали конкретного звена
        PUT    /api/network-nodes/{id}/     - Полное обновление звена
        PATCH  /api/network-nodes/{id}/     - Частичное обновление звена
        DELETE /api/network-nodes/{id}/     - Удалить звено
        GET    /api/network-nodes/statistics/ - Статистика по сети (кастомный action)
    """

    queryset = NetworkNode.objects.all()
    permission_classes = [IsActiveEmployee]  # Только активные сотрудники (ТЗ)
    filterset_class = NetworkNodeFilter  # Фильтрация по стране и др. (ТЗ)
    search_fields = ['name', 'email', 'city', 'country']  # Поля для текстового поиска
    ordering_fields = ['name', 'hierarchy_level', 'debt', 'created_at']  # Поля для сортировки
    ordering = ['hierarchy_level', 'name']  # Сортировка по умолчанию

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора в зависимости от действия.

        - list: упрощенный сериализатор без вложенных данных
        - retrieve: подробный сериализатор с продуктами
        - create/update: сериализатор с запретом изменения долга

        Returns:
            Класс сериализатора
        """
        if self.action == 'list':
            return NetworkNodeListSerializer
        elif self.action == 'retrieve':
            return NetworkNodeDetailSerializer
        else:  # create, update, partial_update
            return NetworkNodeCreateUpdateSerializer

    def get_queryset(self):
        """
        Возвращает оптимизированный QuerySet.

        Используем select_related для предзагрузки связанных объектов
        и prefetch_related для оптимизации загрузки продуктов.
        Это предотвращает проблему N+1 запросов.

        Returns:
            Оптимизированный QuerySet
        """
        queryset = super().get_queryset()

        # Для списка и детального просмотра загружаем поставщика
        if self.action in ['list', 'retrieve']:
            queryset = queryset.select_related('supplier')

        # Для детального просмотра также загружаем продукты
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related('products')

        return queryset

    def update(self, request, *args, **kwargs):
        """
        Обновление звена сети (PUT/PATCH).

        ВАЖНО: Переопределяем метод для явной проверки попытки изменить debt.
        Если пользователь пытается изменить debt, возвращаем ошибку с понятным сообщением.

        Args:
            request: HTTP запрос

        Returns:
            Response с обновленными данными или ошибкой
        """
        # Проверяем, пытается ли пользователь изменить долг
        if 'debt' in request.data:
            return Response(
                {
                    'error': 'Обновление поля "debt" через API запрещено.',
                    'detail': 'Задолженность можно изменить только через админ-панель.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Если долг не пытаются изменить, выполняем стандартное обновление
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Частичное обновление звена сети (PATCH).

        Та же логика проверки debt, что и в update.

        Args:
            request: HTTP запрос

        Returns:
            Response с обновленными данными или ошибкой
        """
        if 'debt' in request.data:
            return Response(
                {
                    'error': 'Обновление поля "debt" через API запрещено.',
                    'detail': 'Задолженность можно изменить только через админ-панель.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().partial_update(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Кастомный endpoint для получения статистики по торговой сети.

        Endpoint: GET /api/network-nodes/statistics/

        Возвращает агрегированную статистику:
        - Общее количество звеньев
        - Количество заводов, сетей, ИП
        - Общую задолженность
        - Средний уровень иерархии

        Args:
            request: HTTP запрос

        Returns:
            Response со статистикой
        """
        # Получаем агрегированные данные одним запросом
        stats = NetworkNode.objects.aggregate(
            total_nodes=Count('id'),
            total_factories=Count('id', filter=models.Q(node_type=NetworkNode.NodeType.FACTORY)),
            total_retail_networks=Count('id', filter=models.Q(node_type=NetworkNode.NodeType.RETAIL_NETWORK)),
            total_entrepreneurs=Count('id', filter=models.Q(node_type=NetworkNode.NodeType.ENTREPRENEUR)),
            total_debt=Sum('debt'),
            average_hierarchy_level=Avg('hierarchy_level'),
        )

        # Обрабатываем None значения
        stats['total_debt'] = stats['total_debt'] or 0
        stats['average_hierarchy_level'] = stats['average_hierarchy_level'] or 0

        serializer = NetworkNodeStatisticsSerializer(stats)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def clear_debt(self, request, pk=None):
        """
        Кастомный endpoint для очистки задолженности конкретного звена.

        Endpoint: POST /api/network-nodes/{id}/clear_debt/

        Этот метод позволяет обнулить задолженность через API,
        но требует явного POST запроса (не просто обновление).

        Args:
            request: HTTP запрос
            pk: ID звена сети

        Returns:
            Response с обновленными данными
        """
        network_node = self.get_object()
        network_node.clear_debt()

        serializer = self.get_serializer(network_node)
        return Response({
            'message': 'Задолженность успешно очищена.',
            'data': serializer.data
        })


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления продуктами.

    Предоставляет CRUD операции для продуктов электроники.

    Endpoints:
        GET    /api/products/          - Список всех продуктов
        POST   /api/products/          - Создать новый продукт
        GET    /api/products/{id}/     - Детали конкретного продукта
        PUT    /api/products/{id}/     - Полное обновление продукта
        PATCH  /api/products/{id}/     - Частичное обновление продукта
        DELETE /api/products/{id}/     - Удалить продукт
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee]  # Только активные сотрудники
    filterset_class = ProductFilter
    search_fields = ['name', 'model']
    ordering_fields = ['name', 'release_date']
    ordering = ['-release_date', 'name']  # Новые продукты сначала

    def get_queryset(self):
        """
        Возвращает оптимизированный QuerySet с предзагрузкой звена сети.

        Returns:
            Оптимизированный QuerySet
        """
        queryset = super().get_queryset()
        # Загружаем связанное звено сети одним запросом
        return queryset.select_related('network_node')


# Импортируем Q для фильтрации в statistics
from django.db import models