"""
Скрипт для начальной настройки базы данных.

Этот скрипт создает тестовые данные для демонстрации работы системы.
Запускайте его после выполнения миграций.
"""

import os
import sys
from datetime import date, timedelta
from decimal import Decimal

import django

# Настройка Django окружения
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electronics_network.settings')
django.setup()

from django.contrib.auth import get_user_model
from network.models import NetworkNode, Product

User = get_user_model()


def create_test_users():
    """Создает тестовых пользователей."""
    print("Создание тестовых пользователей...")

    # Создаем суперпользователя для доступа к админке
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@electronicsnetwork.local',
            password='admin123'
        )
        print(f"✓ Создан администратор: {admin.username}")
    else:
        print("✓ Администратор уже существует")

    # Создаем обычного активного сотрудника
    if not User.objects.filter(username='employee').exists():
        employee = User.objects.create_user(
            username='employee',
            email='employee@electronicsnetwork.local',
            password='employee123',
            is_active=True,
            is_staff=False
        )
        print(f"✓ Создан сотрудник: {employee.username}")
    else:
        print("✓ Сотрудник уже существует")


def create_test_network():
    """Создает тестовую иерархию торговой сети."""
    print("\nСоздание тестовой торговой сети...")

    # Создаем заводы (уровень 0)
    factory_samsung, _ = NetworkNode.objects.get_or_create(
        name='Завод Samsung Electronics',
        defaults={
            'node_type': NetworkNode.NodeType.FACTORY,
            'email': 'contact@samsung.com',
            'country': 'Южная Корея',
            'city': 'Сеул',
            'street': 'Seocho-daero',
            'house_number': '1321',
            'debt': Decimal('0.00')
        }
    )
    print(f"✓ Завод Samsung (уровень {factory_samsung.hierarchy_level})")

    factory_apple, _ = NetworkNode.objects.get_or_create(
        name='Завод Apple Inc',
        defaults={
            'node_type': NetworkNode.NodeType.FACTORY,
            'email': 'manufacturing@apple.com',
            'country': 'США',
            'city': 'Купертино',
            'street': 'Apple Park Way',
            'house_number': '1',
            'debt': Decimal('0.00')
        }
    )
    print(f"✓ Завод Apple (уровень {factory_apple.hierarchy_level})")

    factory_xiaomi, _ = NetworkNode.objects.get_or_create(
        name='Завод Xiaomi',
        defaults={
            'node_type': NetworkNode.NodeType.FACTORY,
            'email': 'factory@xiaomi.com',
            'country': 'Китай',
            'city': 'Пекин',
            'street': 'Qinghe Middle Street',
            'house_number': '68',
            'debt': Decimal('0.00')
        }
    )
    print(f"✓ Завод Xiaomi (уровень {factory_xiaomi.hierarchy_level})")

    # Создаем розничные сети (уровень 1)
    mvideo, _ = NetworkNode.objects.get_or_create(
        name='М.Видео',
        defaults={
            'node_type': NetworkNode.NodeType.RETAIL_NETWORK,
            'email': 'info@mvideo.ru',
            'country': 'Россия',
            'city': 'Москва',
            'street': 'Тверская',
            'house_number': '1',
            'supplier': factory_samsung,
            'debt': Decimal('1500000.50')
        }
    )
    print(f"✓ М.Видео (уровень {mvideo.hierarchy_level})")

    dns, _ = NetworkNode.objects.get_or_create(
        name='DNS',
        defaults={
            'node_type': NetworkNode.NodeType.RETAIL_NETWORK,
            'email': 'info@dns-shop.ru',
            'country': 'Россия',
            'city': 'Владивосток',
            'street': 'Океанский проспект',
            'house_number': '17',
            'supplier': factory_apple,
            'debt': Decimal('2300000.00')
        }
    )
    print(f"✓ DNS (уровень {dns.hierarchy_level})")

    eldorado, _ = NetworkNode.objects.get_or_create(
        name='Эльдорадо',
        defaults={
            'node_type': NetworkNode.NodeType.RETAIL_NETWORK,
            'email': 'contact@eldorado.ru',
            'country': 'Россия',
            'city': 'Санкт-Петербург',
            'street': 'Невский проспект',
            'house_number': '100',
            'supplier': factory_xiaomi,
            'debt': Decimal('980000.75')
        }
    )
    print(f"✓ Эльдорадо (уровень {eldorado.hierarchy_level})")

    # Создаем ИП (уровень 2)
    ip_ivanov, _ = NetworkNode.objects.get_or_create(
        name='ИП Иванов И.И.',
        defaults={
            'node_type': NetworkNode.NodeType.ENTREPRENEUR,
            'email': 'ivanov@mail.ru',
            'country': 'Россия',
            'city': 'Казань',
            'street': 'Баумана',
            'house_number': '58',
            'supplier': mvideo,
            'debt': Decimal('150000.00')
        }
    )
    print(f"✓ ИП Иванов (уровень {ip_ivanov.hierarchy_level})")

    ip_petrov, _ = NetworkNode.objects.get_or_create(
        name='ИП Петров П.П.',
        defaults={
            'node_type': NetworkNode.NodeType.ENTREPRENEUR,
            'email': 'petrov@yandex.ru',
            'country': 'Россия',
            'city': 'Екатеринбург',
            'street': 'Ленина',
            'house_number': '25',
            'supplier': dns,
            'debt': Decimal('75000.50')
        }
    )
    print(f"✓ ИП Петров (уровень {ip_petrov.hierarchy_level})")

    ip_sidorov, _ = NetworkNode.objects.get_or_create(
        name='ИП Сидоров С.С.',
        defaults={
            'node_type': NetworkNode.NodeType.ENTREPRENEUR,
            'email': 'sidorov@gmail.com',
            'country': 'Россия',
            'city': 'Новосибирск',
            'street': 'Красный проспект',
            'house_number': '1',
            'supplier': eldorado,
            'debt': Decimal('50000.00')
        }
    )
    print(f"✓ ИП Сидоров (уровень {ip_sidorov.hierarchy_level})")

    return {
        'factories': [factory_samsung, factory_apple, factory_xiaomi],
        'retail': [mvideo, dns, eldorado],
        'entrepreneurs': [ip_ivanov, ip_petrov, ip_sidorov]
    }


def create_test_products(nodes):
    """Создает тестовые продукты."""
    print("\nСоздание тестовых продуктов...")

    today = date.today()

    # Продукты Samsung
    products_samsung = [
        ('Смартфон', 'Galaxy S23', today - timedelta(days=300)),
        ('Смартфон', 'Galaxy A54', today - timedelta(days=200)),
        ('Телевизор', 'QLED 4K 55"', today - timedelta(days=400)),
        ('Холодильник', 'RB38', today - timedelta(days=500)),
    ]

    for name, model, release_date in products_samsung:
        Product.objects.get_or_create(
            network_node=nodes['factories'][0],
            name=name,
            model=model,
            defaults={'release_date': release_date}
        )
        print(f"  ✓ {name} {model}")

    # Продукты Apple
    products_apple = [
        ('Смартфон', 'iPhone 15 Pro', today - timedelta(days=150)),
        ('Смартфон', 'iPhone 15', today - timedelta(days=150)),
        ('Ноутбук', 'MacBook Pro 16"', today - timedelta(days=250)),
        ('Планшет', 'iPad Pro', today - timedelta(days=180)),
        ('Наушники', 'AirPods Pro 2', today - timedelta(days=365)),
    ]

    for name, model, release_date in products_apple:
        Product.objects.get_or_create(
            network_node=nodes['factories'][1],
            name=name,
            model=model,
            defaults={'release_date': release_date}
        )
        print(f"  ✓ {name} {model}")

    # Продукты Xiaomi
    products_xiaomi = [
        ('Смартфон', 'Redmi Note 13 Pro', today - timedelta(days=100)),
        ('Смартфон', 'Mi 13 Ultra', today - timedelta(days=280)),
        ('Пылесос', 'Robot Vacuum S10+', today - timedelta(days=220)),
        ('Электросамокат', 'Mi Scooter 4 Pro', today - timedelta(days=320)),
    ]

    for name, model, release_date in products_xiaomi:
        Product.objects.get_or_create(
            network_node=nodes['factories'][2],
            name=name,
            model=model,
            defaults={'release_date': release_date}
        )
        print(f"  ✓ {name} {model}")


def main():
    """Главная функция."""
    print("=" * 60)
    print("ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ")
    print("=" * 60)

    try:
        # Создаем пользователей
        create_test_users()

        # Создаем торговую сеть
        nodes = create_test_network()

        # Создаем продукты
        create_test_products(nodes)

        print("\n" + "=" * 60)
        print("✓ БАЗА ДАННЫХ УСПЕШНО ИНИЦИАЛИЗИРОВАНА!")
        print("=" * 60)
        print("\nДанные для входа:")
        print("  Администратор:")
        print("    Логин: admin")
        print("    Пароль: admin123")
        print("  Сотрудник (для API):")
        print("    Логин: employee")
        print("    Пароль: employee123")
        print("\nДоступные URL:")
        print("  Админ-панель: http://localhost:8000/admin/")
        print("  API: http://localhost:8000/api/")
        print("  Swagger: http://localhost:8000/swagger/")
        print("  ReDoc: http://localhost:8000/redoc/")

    except Exception as e:
        print(f"\n✗ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()