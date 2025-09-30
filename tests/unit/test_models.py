"""
Юнит-тесты для моделей приложения network.

Эти тесты проверяют корректность работы моделей NetworkNode и Product.
"""

import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from network.models import NetworkNode, Product


@pytest.mark.django_db
class TestNetworkNodeModel:
    """Тесты для модели NetworkNode."""

    def test_create_factory_node(self):
        """Тест создания завода (уровень 0)."""
        factory = NetworkNode.objects.create(
            name='Завод Xiaomi',
            node_type=NetworkNode.NodeType.FACTORY,
            email='xiaomi@factory.com',
            country='Китай',
            city='Пекин',
            street='Beijing Road',
            house_number='100',
            supplier=None
        )

        assert factory.id is not None
        assert factory.hierarchy_level == 0
        assert factory.debt == Decimal('0.00')
        assert factory.supplier is None

    def test_create_retail_network_with_supplier(self, factory_node):
        """Тест создания розничной сети с поставщиком."""
        retail = NetworkNode.objects.create(
            name='Эльдорадо',
            node_type=NetworkNode.NodeType.RETAIL_NETWORK,
            email='info@eldorado.ru',
            country='Россия',
            city='Москва',
            street='Ленинский проспект',
            house_number='30',
            supplier=factory_node,
            debt=100000.00
        )

        assert retail.hierarchy_level == 1  # Уровень поставщика + 1
        assert retail.supplier == factory_node
        assert retail.debt == Decimal('100000.00')

    def test_hierarchy_level_calculation(self, factory_node):
        """Тест автоматического расчета уровня иерархии."""
        # Создаем цепочку: Завод -> Сеть1 -> Сеть2 -> ИП

        retail1 = NetworkNode.objects.create(
            name='Сеть 1',
            node_type=NetworkNode.NodeType.RETAIL_NETWORK,
            email='retail1@test.com',
            country='Россия',
            city='Москва',
            street='Улица 1',
            house_number='1',
            supplier=factory_node
        )
        assert retail1.hierarchy_level == 1

        retail2 = NetworkNode.objects.create(
            name='Сеть 2',
            node_type=NetworkNode.NodeType.RETAIL_NETWORK,
            email='retail2@test.com',
            country='Россия',
            city='Москва',
            street='Улица 2',
            house_number='2',
            supplier=retail1
        )
        assert retail2.hierarchy_level == 2

        ie = NetworkNode.objects.create(
            name='ИП',
            node_type=NetworkNode.NodeType.ENTREPRENEUR,
            email='ie@test.com',
            country='Россия',
            city='Москва',
            street='Улица 3',
            house_number='3',
            supplier=retail2
        )
        assert ie.hierarchy_level == 3

    def test_str_representation(self, factory_node):
        """Тест строкового представления модели."""
        expected = f"{factory_node.name} (уровень {factory_node.hierarchy_level})"
        assert str(factory_node) == expected

    def test_get_full_address(self, factory_node):
        """Тест получения полного адреса."""
        expected = "Южная Корея, Сеул, Тэхэран-ро, дом 123"
        assert factory_node.get_full_address() == expected

    def test_clear_debt(self, retail_node):
        """Тест очистки задолженности."""
        # Проверяем, что изначально есть долг
        assert retail_node.debt > 0

        # Очищаем долг
        retail_node.clear_debt()

        # Проверяем, что долг обнулен
        retail_node.refresh_from_db()
        assert retail_node.debt == Decimal('0.00')

    def test_debt_default_value(self):
        """Тест значения задолженности по умолчанию."""
        node = NetworkNode.objects.create(
            name='Тест',
            node_type=NetworkNode.NodeType.FACTORY,
            email='test@test.com',
            country='Страна',
            city='Город',
            street='Улица',
            house_number='1'
        )

        assert node.debt == Decimal('0.00')

    def test_created_at_auto_filled(self, factory_node):
        """Тест автоматического заполнения created_at."""
        assert factory_node.created_at is not None

    def test_updated_at_auto_updates(self, factory_node):
        """Тест автоматического обновления updated_at."""
        old_updated_at = factory_node.updated_at

        # Изменяем объект
        factory_node.name = 'Новое название'
        factory_node.save()

        # Проверяем, что updated_at обновился
        assert factory_node.updated_at > old_updated_at


@pytest.mark.django_db
class TestProductModel:
    """Тесты для модели Product."""

    def test_create_product(self, factory_node):
        """Тест создания продукта."""
        product = Product.objects.create(
            network_node=factory_node,
            name='Телевизор',
            model='QLED 4K',
            release_date='2023-05-15'
        )

        assert product.id is not None
        assert product.network_node == factory_node
        assert product.name == 'Телевизор'
        assert product.model == 'QLED 4K'

    def test_str_representation(self, product):
        """Тест строкового представления продукта."""
        expected = f"{product.name} {product.model} ({product.release_date})"
        assert str(product) == expected

    def test_product_relationship_with_node(self, factory_node, product):
        """Тест связи продукта со звеном сети."""
        # Проверяем обратную связь
        products = factory_node.products.all()
        assert product in products
        assert products.count() == 1

    def test_cascade_delete(self, factory_node, product):
        """Тест каскадного удаления продуктов при удалении звена."""
        product_id = product.id

        # Удаляем звено сети
        factory_node.delete()

        # Проверяем, что продукт тоже удален
        assert not Product.objects.filter(id=product_id).exists()

    def test_unique_together_constraint(self, factory_node):
        """Тест уникальности комбинации (network_node, name, model)."""
        # Создаем первый продукт
        Product.objects.create(
            network_node=factory_node,
            name='Смартфон',
            model='Model X',
            release_date='2023-01-01'
        )

        # Пытаемся создать дубликат
        with pytest.raises(IntegrityError):
            Product.objects.create(
                network_node=factory_node,
                name='Смартфон',
                model='Model X',
                release_date='2023-12-31'  # Другая дата, но та же комбинация name+model
            )