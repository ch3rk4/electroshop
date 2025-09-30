"""
Интеграционные тесты для API торговой сети.

Эти тесты проверяют работу API endpoints, включая аутентификацию,
права доступа, CRUD операции и фильтрацию.
"""

import pytest
from decimal import Decimal
from rest_framework import status

from network.models import NetworkNode, Product


@pytest.mark.django_db
class TestNetworkNodeAPI:
    """Тесты для API звеньев сети."""

    def test_list_nodes_unauthorized(self, api_client, factory_node):
        """Тест получения списка без аутентификации - должен вернуть 403."""
        url = '/api/network-nodes/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_nodes_inactive_user(self, api_client, inactive_user, factory_node):
        """Тест получения списка неактивным пользователем - должен вернуть 403."""
        api_client.force_authenticate(user=inactive_user)
        url = '/api/network-nodes/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_nodes_authenticated(self, authenticated_client, factory_node, retail_node):
        """Тест получения списка звеньев активным пользователем."""
        url = '/api/network-nodes/'
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2

    def test_retrieve_node_detail(self, authenticated_client, factory_node, product):
        """Тест получения детальной информации о звене."""
        url = f'/api/network-nodes/{factory_node.id}/'
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == factory_node.name
        assert response.data['hierarchy_level'] == 0
        assert len(response.data['products']) == 1

    def test_create_factory_node(self, authenticated_client):
        """Тест создания нового завода через API."""
        url = '/api/network-nodes/'
        data = {
            'name': 'Новый завод',
            'node_type': 'FACTORY',
            'email': 'new@factory.com',
            'country': 'Германия',
            'city': 'Берлин',
            'street': 'Hauptstrasse',
            'house_number': '50',
            'supplier': None
        }
        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Новый завод'
        assert response.data['hierarchy_level'] == 0

        # Проверяем, что объект создан в БД
        assert NetworkNode.objects.filter(name='Новый завод').exists()

    def test_create_retail_with_supplier(self, authenticated_client, factory_node):
        """Тест создания розничной сети с поставщиком."""
        url = '/api/network-nodes/'
        data = {
            'name': 'Новая сеть',
            'node_type': 'RETAIL',
            'email': 'new@retail.com',
            'country': 'Россия',
            'city': 'Казань',
            'street': 'Баумана',
            'house_number': '10',
            'supplier': factory_node.id
        }
        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['supplier'] == factory_node.id

    def test_update_node_without_debt(self, authenticated_client, retail_node):
        """Тест обновления звена без изменения долга."""
        url = f'/api/network-nodes/{retail_node.id}/'
        data = {
            'name': 'Обновленное название',
            'node_type': retail_node.node_type,
            'email': retail_node.email,
            'country': retail_node.country,
            'city': 'Новый город',
            'street': retail_node.street,
            'house_number': retail_node.house_number,
            'supplier': retail_node.supplier.id
        }
        response = authenticated_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Обновленное название'
        assert response.data['city'] == 'Новый город'

        # Проверяем, что долг НЕ изменился
        retail_node.refresh_from_db()
        assert retail_node.debt == Decimal('150000.50')

    def test_update_node_with_debt_forbidden(self, authenticated_client, retail_node):
        """Тест запрета обновления долга через API (ТРЕБОВАНИЕ ТЗ)."""
        url = f'/api/network-nodes/{retail_node.id}/'
        original_debt = retail_node.debt

        data = {
            'name': retail_node.name,
            'node_type': retail_node.node_type,
            'email': retail_node.email,
            'country': retail_node.country,
            'city': retail_node.city,
            'street': retail_node.street,
            'house_number': retail_node.house_number,
            'supplier': retail_node.supplier.id,
            'debt': '999999.99'  # Пытаемся изменить долг
        }
        response = authenticated_client.put(url, data, format='json')

        # Должна быть ошибка 400
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

        # Проверяем, что долг НЕ изменился в БД
        retail_node.refresh_from_db()
        assert retail_node.debt == original_debt

    def test_partial_update_with_debt_forbidden(self, authenticated_client, retail_node):
        """Тест запрета частичного обновления с изменением долга."""
        url = f'/api/network-nodes/{retail_node.id}/'
        original_debt = retail_node.debt

        data = {
            'debt': '0.00'  # Пытаемся обнулить долг через PATCH
        }
        response = authenticated_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Долг не должен измениться
        retail_node.refresh_from_db()
        assert retail_node.debt == original_debt

    def test_delete_node(self, authenticated_client, entrepreneur_node):
        """Тест удаления звена сети."""
        url = f'/api/network-nodes/{entrepreneur_node.id}/'
        node_id = entrepreneur_node.id

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not NetworkNode.objects.filter(id=node_id).exists()

    def test_filter_by_country(self, authenticated_client, factory_node, multiple_nodes):
        """Тест фильтрации по стране (ТРЕБОВАНИЕ ТЗ)."""
        url = '/api/network-nodes/?country=Россия'
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        # Должны быть только российские звенья
        for node in response.data['results']:
            assert node['country'] == 'Россия'

    def test_filter_by_city(self, authenticated_client, factory_node, retail_node):
        """Тест фильтрации по городу."""
        url = '/api/network-nodes/?city=Москва'
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['city'] == 'Москва'

    def test_clear_debt_action(self, authenticated_client, retail_node):
        """Тест специального endpoint для очистки долга."""
        url = f'/api/network-nodes/{retail_node.id}/clear_debt/'

        # Проверяем, что долг есть
        assert retail_node.debt > 0

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data

        # Проверяем, что долг очищен
        retail_node.refresh_from_db()
        assert retail_node.debt == Decimal('0.00')

    def test_statistics_endpoint(self, authenticated_client, factory_node, retail_node, entrepreneur_node):
        """Тест endpoint статистики."""
        url = '/api/network-nodes/statistics/'
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'total_nodes' in response.data
        assert 'total_factories' in response.data
        assert 'total_debt' in response.data
        assert response.data['total_nodes'] == 3


@pytest.mark.django_db
class TestProductAPI:
    """Тесты для API продуктов."""

    def test_list_products_unauthorized(self, api_client, product):
        """Тест получения списка продуктов без аутентификации."""
        url = '/api/products/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_products_authenticated(self, authenticated_client, product):
        """Тест получения списка продуктов активным пользователем."""
        url = '/api/products/'
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_create_product(self, authenticated_client, factory_node):
        """Тест создания продукта через API."""
        url = '/api/products/'
        data = {
            'network_node': factory_node.id,
            'name': 'Ноутбук',
            'model': 'ThinkPad X1',
            'release_date': '2023-06-01'
        }
        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Ноутбук'

        # Проверяем создание в БД
        assert Product.objects.filter(name='Ноутбук', model='ThinkPad X1').exists()

    def test_update_product(self, authenticated_client, product):
        """Тест обновления продукта."""
        url = f'/api/products/{product.id}/'
        data = {
            'name': 'Обновленный смартфон',
            'model': product.model,
            'release_date': product.release_date
        }
        response = authenticated_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Обновленный смартфон'

    def test_delete_product(self, authenticated_client, product):
        """Тест удаления продукта."""
        url = f'/api/products/{product.id}/'
        product_id = product.id

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Product.objects.filter(id=product_id).exists()