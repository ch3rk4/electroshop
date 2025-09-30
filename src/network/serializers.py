"""
Сериализаторы для API торговой сети.

Сериализаторы преобразуют модели Django в JSON (и обратно) для API.
Они также отвечают за валидацию входящих данных.
"""

from rest_framework import serializers

from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.

    Используется для отображения и создания продуктов через API.
    """

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'model',
            'release_date',
        ]
        read_only_fields = ['id']


class NetworkNodeListSerializer(serializers.ModelSerializer):
    """
    Упрощенный сериализатор для списка звеньев сети.

    Используется в list views для отображения краткой информации.
    Не включает вложенные продукты для оптимизации производительности.
    """

    supplier_name = serializers.CharField(
        source='supplier.name',
        read_only=True,
        help_text='Название поставщика'
    )

    class Meta:
        model = NetworkNode
        fields = [
            'id',
            'name',
            'node_type',
            'email',
            'country',
            'city',
            'supplier',
            'supplier_name',
            'hierarchy_level',
            'debt',
            'created_at',
        ]
        read_only_fields = ['id', 'hierarchy_level', 'created_at']


class NetworkNodeDetailSerializer(serializers.ModelSerializer):
    """
    Подробный сериализатор для звена сети.

    Используется для детального просмотра (retrieve) и включает
    все поля модели, включая список продуктов.
    """

    # Вложенный сериализатор для отображения списка продуктов
    products = ProductSerializer(many=True, read_only=True)

    # Отображаем название поставщика для удобства
    supplier_name = serializers.CharField(
        source='supplier.name',
        read_only=True,
        allow_null=True,
        help_text='Название поставщика (null для заводов)'
    )

    # Добавляем полный адрес как computed field
    full_address = serializers.SerializerMethodField(
        help_text='Полный адрес в читаемом формате'
    )

    class Meta:
        model = NetworkNode
        fields = [
            'id',
            'name',
            'node_type',
            'email',
            'country',
            'city',
            'street',
            'house_number',
            'full_address',
            'supplier',
            'supplier_name',
            'hierarchy_level',
            'debt',
            'products',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'hierarchy_level',
            'created_at',
            'updated_at',
        ]

    def get_full_address(self, obj: NetworkNode) -> str:
        """
        Возвращает полный адрес звена сети.

        Args:
            obj: Объект NetworkNode

        Returns:
            Полный адрес в формате "Страна, Город, Улица, дом Номер"
        """
        return obj.get_full_address()


class NetworkNodeCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления звена сети.

    Этот сериализатор имеет критическое ограничение (ТРЕБОВАНИЕ ТЗ):
    поле 'debt' (задолженность) НЕ может быть обновлено через API.
    Оно доступно только для чтения.
    """

    class Meta:
        model = NetworkNode
        fields = [
            'id',
            'name',
            'node_type',
            'email',
            'country',
            'city',
            'street',
            'house_number',
            'supplier',
            'debt',  # Включено в поля, но будет read_only
        ]
        read_only_fields = [
            'id',
            'debt',  # ВАЖНО: Долг НЕ редактируется через API (требование ТЗ)
        ]

    def validate_supplier(self, value):
        """
        Валидация поставщика.

        Проверяем, что звено не ссылается само на себя как на поставщика
        (это создало бы циклическую зависимость).

        Args:
            value: Значение поля supplier

        Returns:
            Валидированное значение

        Raises:
            ValidationError: Если валидация не прошла
        """
        # При создании нового объекта self.instance будет None
        if self.instance and value and value.id == self.instance.id:
            raise serializers.ValidationError(
                'Звено сети не может быть поставщиком само себе.'
            )
        return value

    def validate(self, attrs):
        """
        Общая валидация данных.

        Проверяем бизнес-логику: например, завод не должен иметь поставщика.

        Args:
            attrs: Словарь с валидируемыми атрибутами

        Returns:
            Валидированные атрибуты

        Raises:
            ValidationError: Если валидация не прошла
        """
        node_type = attrs.get('node_type', self.instance.node_type if self.instance else None)
        supplier = attrs.get('supplier', self.instance.supplier if self.instance else None)

        # Завод не должен иметь поставщика
        if node_type == NetworkNode.NodeType.FACTORY and supplier is not None:
            raise serializers.ValidationError({
                'supplier': 'Завод не может иметь поставщика. Завод - верхний уровень иерархии.'
            })

        # Розничная сеть и ИП должны иметь поставщика
        if node_type in [NetworkNode.NodeType.RETAIL_NETWORK, NetworkNode.NodeType.ENTREPRENEUR]:
            if supplier is None:
                raise serializers.ValidationError({
                    'supplier': 'Розничная сеть и ИП должны иметь поставщика.'
                })

        return attrs


class NetworkNodeStatisticsSerializer(serializers.Serializer):
    """
    Сериализатор для статистики по торговой сети.

    Может использоваться для endpoint'а, который возвращает аналитику.
    """

    total_nodes = serializers.IntegerField(
        help_text='Общее количество звеньев в сети'
    )
    total_factories = serializers.IntegerField(
        help_text='Количество заводов'
    )
    total_retail_networks = serializers.IntegerField(
        help_text='Количество розничных сетей'
    )
    total_entrepreneurs = serializers.IntegerField(
        help_text='Количество индивидуальных предпринимателей'
    )
    total_debt = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text='Общая задолженность по всей сети'
    )
    average_hierarchy_level = serializers.FloatField(
        help_text='Средний уровень иерархии'
    )