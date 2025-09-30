"""
Конфигурация pytest и фикстуры для тестов.

Этот файл содержит общие фикстуры, которые используются во всех тестах.
Фикстуры - это переиспользуемые компоненты для настройки тестового окружения.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from network.models import NetworkNode, Product

User = get_user_model()


@pytest.fixture
def api_client():
    """
    Фикстура для создания API клиента.

    Returns:
        APIClient: Клиент для тестирования API
    """
    return APIClient()


@pytest.fixture
def active_user(db):
    """
    Фикстура для создания активного пользователя.

    Args:
        db: Фикстура pytest-django для доступа к БД

    Returns:
        User: Активный пользователь
    """
    user = User.objects.create_user(
        username='activeuser',
        email='active@test.com',
        password='testpass123',
        is_active=True,
        is_staff=False
    )
    return user


@pytest.fixture
def inactive_user(db):
    """
    Фикстура для создания неактивного пользователя.

    Args:
        db: Фикстура pytest-django для доступа к БД

    Returns:
        User: Неактивный пользователь
    """
    user = User.objects.create_user(
        username='inactiveuser',
        email='inactive@test.com',
        password='testpass123',
        is_active=False,
        is_staff=False
    )
    return user


@pytest.fixture
def admin_user(db):
    """
    Фикстура для создания администратора.

    Args:
        db: Фикстура pytest-django для доступа к БД

    Returns:
        User: Пользователь с правами администратора
    """
    user = User.objects.create_user(
        username='admin',
        email='admin@test.com',
        password='adminpass123',
        is_active=True,
        is_staff=True,
        is_superuser=True
    )
    return user


@pytest.fixture
def authenticated_client(api_client, active_user):
    """
    Фикстура для создания аутентифицированного API клиента.

    Args:
        api_client: API клиент
        active_user: Активный пользователь

    Returns:
        APIClient: Аутентифицированный клиент
    """
    api_client.force_authenticate(user=active_user)
    return api_client


@pytest.fixture
def factory_node(db):
    """
    Фикстура для создания завода (уровень 0).

    Args:
        db: Фикстура pytest-django для доступа к БД

    Returns:
        NetworkNode: Объект завода
    """
    return NetworkNode.objects.create(
        name='Завод Samsung',
        node_type=NetworkNode.NodeType.FACTORY,
        email='samsung@factory.com',
        country='Южная Корея',
        city='Сеул',
        street='Тэхэран-ро',
        house_number='123',
        supplier=None,  # Завод не имеет поставщика
        debt=0.00
    )


@pytest.fixture
def retail_node(db, factory_node):
    """
    Фикстура для создания розничной сети (уровень 1).

    Args:
        db: Фикстура pytest-django для доступа к БД
        factory_node: Завод-поставщик

    Returns:
        NetworkNode: Объект розничной сети
    """
    return NetworkNode.objects.create(
        name='М.Видео',
        node_type=NetworkNode.NodeType.RETAIL_NETWORK,
        email='info@mvideo.ru',
        country='Россия',
        city='Москва',
        street='Тверская',
        house_number='1',
        supplier=factory_node,
        debt=150000.50
    )


@pytest.fixture
def entrepreneur_node(db, retail_node):
    """
    Фикстура для создания ИП (уровень 2).

    Args:
        db: Фикстура pytest-django для доступа к БД
        retail_node: Розничная сеть-поставщик

    Returns:
        NetworkNode: Объект ИП
    """
    return NetworkNode.objects.create(
        name='ИП Иванов',
        node_type=NetworkNode.NodeType.ENTREPRENEUR,
        email='ivanov@ip.ru',
        country='Россия',
        city='Санкт-Петербург',
        street='Невский проспект',
        house_number='50',
        supplier=retail_node,
        debt=25000.00
    )


@pytest.fixture
def product(db, factory_node):
    """
    Фикстура для создания продукта.

    Args:
        db: Фикстура pytest-django для доступа к БД
        factory_node: Звено сети, которому принадлежит продукт

    Returns:
        Product: Объект продукта
    """
    return Product.objects.create(
        network_node=factory_node,
        name='Смартфон',
        model='Galaxy S21',
        release_date='2021-01-29'
    )


@pytest.fixture
def multiple_nodes(db, factory_node):
    """
    Фикстура для создания нескольких звеньев сети для тестирования списков.

    Args:
        db: Фикстура pytest-django для доступа к БД
        factory_node: Завод-поставщик

    Returns:
        list: Список созданных звеньев сети
    """
    nodes = []

    # Создаем еще один завод
    factory2 = NetworkNode.objects.create(
        name='Завод Apple',
        node_type=NetworkNode.NodeType.FACTORY,
        email='apple@factory.com',
        country='США',
        city='Купертино',
        street='Apple Park Way',
        house_number='1',
        supplier=None,
        debt=0.00
    )
    nodes.append(factory2)

    # Создаем розничную сеть для второго завода
    retail2 = NetworkNode.objects.create(
        name='DNS',
        node_type=NetworkNode.NodeType.RETAIL_NETWORK,
        email='info@dns-shop.ru',
        country='Россия',
        city='Владивосток',
        street='Океанский проспект',
        house_number='10',
        supplier=factory2,
        debt=200000.00
    )
    nodes.append(retail2)

    # Создаем ИП
    ie = NetworkNode.objects.create(
        name='ИП Петров',
        node_type=NetworkNode.NodeType.ENTREPRENEUR,
        email='petrov@ip.ru',
        country='Россия',
        city='Москва',
        street='Арбат',
        house_number='20',
        supplier=retail2,
        debt=50000.00
    )
    nodes.append(ie)

    return nodes