"""
Фильтры для API торговой сети.

Этот модуль определяет фильтры, которые позволяют пользователям API
искать и фильтровать звенья сети по различным критериям.
"""

import django_filters
from django.db.models import Q

from .models import NetworkNode, Product


class NetworkNodeFilter(django_filters.FilterSet):
    """
    Фильтр для модели NetworkNode.

    Позволяет фильтровать звенья сети по:
    - Стране (точное совпадение) - ТРЕБОВАНИЕ ТЗ
    - Городу (точное совпадение или частичное)
    - Типу звена
    - Уровню иерархии
    - Наличию поставщика
    - Диапазону задолженности
    """

    # Фильтр по стране (ТРЕБОВАНИЕ ТЗ: "по определенной стране")
    # Используем точное совпадение без учета регистра
    country = django_filters.CharFilter(
        field_name='country',
        lookup_expr='iexact',  # Case-insensitive exact match
        help_text='Фильтр по стране (точное совпадение, регистр не важен)'
    )

    # Дополнительный фильтр для поиска по части названия страны
    country_contains = django_filters.CharFilter(
        field_name='country',
        lookup_expr='icontains',  # Case-insensitive containment
        help_text='Поиск по части названия страны'
    )

    # Фильтр по городу
    city = django_filters.CharFilter(
        field_name='city',
        lookup_expr='iexact',
        help_text='Фильтр по городу (точное совпадение)'
    )

    # Поиск по части названия города
    city_contains = django_filters.CharFilter(
        field_name='city',
        lookup_expr='icontains',
        help_text='Поиск по части названия города'
    )

    # Фильтр по типу звена (завод, сеть, ИП)
    node_type = django_filters.ChoiceFilter(
        field_name='node_type',
        choices=NetworkNode.NodeType.choices,
        help_text='Фильтр по типу звена'
    )

    # Фильтр по уровню иерархии
    hierarchy_level = django_filters.NumberFilter(
        field_name='hierarchy_level',
        help_text='Точный уровень иерархии (0 - завод, 1 - первый уровень, и т.д.)'
    )

    # Фильтр по диапазону уровней иерархии
    hierarchy_level_min = django_filters.NumberFilter(
        field_name='hierarchy_level',
        lookup_expr='gte',
        help_text='Минимальный уровень иерархии'
    )

    hierarchy_level_max = django_filters.NumberFilter(
        field_name='hierarchy_level',
        lookup_expr='lte',
        help_text='Максимальный уровень иерархии'
    )

    # Фильтр по наличию поставщика
    has_supplier = django_filters.BooleanFilter(
        method='filter_has_supplier',
        help_text='True - только с поставщиком, False - только без поставщика (заводы)'
    )

    # Фильтр по конкретному поставщику
    supplier = django_filters.ModelChoiceFilter(
        field_name='supplier',
        queryset=NetworkNode.objects.all(),
        help_text='ID конкретного поставщика'
    )

    # Фильтр по задолженности
    debt_min = django_filters.NumberFilter(
        field_name='debt',
        lookup_expr='gte',
        help_text='Минимальная задолженность'
    )

    debt_max = django_filters.NumberFilter(
        field_name='debt',
        lookup_expr='lte',
        help_text='Максимальная задолженность'
    )

    # Фильтр: только звенья с задолженностью
    has_debt = django_filters.BooleanFilter(
        method='filter_has_debt',
        help_text='True - только с задолженностью (debt > 0)'
    )

    # Поиск по названию
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        help_text='Поиск по названию звена'
    )

    # Фильтр по дате создания
    created_after = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        help_text='Созданы после указанной даты/времени'
    )

    created_before = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte',
        help_text='Созданы до указанной даты/времени'
    )

    class Meta:
        model = NetworkNode
        fields = [
            'country',
            'city',
            'node_type',
            'hierarchy_level',
        ]

    def filter_has_supplier(self, queryset, name, value):
        """
        Фильтрует звенья по наличию поставщика.

        Args:
            queryset: Исходный QuerySet
            name: Имя поля фильтра
            value: True или False

        Returns:
            Отфильтрованный QuerySet
        """
        if value:
            # Только звенья с поставщиком (supplier не NULL)
            return queryset.filter(supplier__isnull=False)
        else:
            # Только заводы (supplier is NULL)
            return queryset.filter(supplier__isnull=True)

    def filter_has_debt(self, queryset, name, value):
        """
        Фильтрует звенья по наличию задолженности.

        Args:
            queryset: Исходный QuerySet
            name: Имя поля фильтра
            value: True или False

        Returns:
            Отфильтрованный QuerySet
        """
        if value:
            # Только звенья с задолженностью (debt > 0)
            return queryset.filter(debt__gt=0)
        else:
            # Только звенья без задолженности (debt = 0)
            return queryset.filter(debt=0)


class ProductFilter(django_filters.FilterSet):
    """
    Фильтр для модели Product.

    Позволяет фильтровать продукты по различным критериям.
    """

    # Поиск по названию продукта
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        help_text='Поиск по названию продукта'
    )

    # Поиск по модели
    model = django_filters.CharFilter(
        field_name='model',
        lookup_expr='icontains',
        help_text='Поиск по модели продукта'
    )

    # Фильтр по звену сети
    network_node = django_filters.ModelChoiceFilter(
        field_name='network_node',
        queryset=NetworkNode.objects.all(),
        help_text='ID звена сети, которому принадлежит продукт'
    )

    # Фильтр по стране звена (через связь)
    country = django_filters.CharFilter(
        field_name='network_node__country',
        lookup_expr='iexact',
        help_text='Страна звена сети'
    )

    # Фильтр по дате выхода продукта
    release_date = django_filters.DateFilter(
        field_name='release_date',
        help_text='Точная дата выхода на рынок'
    )

    release_date_after = django_filters.DateFilter(
        field_name='release_date',
        lookup_expr='gte',
        help_text='Выпущены после указанной даты'
    )

    release_date_before = django_filters.DateFilter(
        field_name='release_date',
        lookup_expr='lte',
        help_text='Выпущены до указанной даты'
    )

    # Фильтр по году выпуска
    release_year = django_filters.NumberFilter(
        field_name='release_date__year',
        help_text='Год выпуска продукта'
    )

    class Meta:
        model = Product
        fields = [
            'name',
            'model',
            'network_node',
            'release_date',
        ]