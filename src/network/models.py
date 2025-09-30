"""
Модели данных для торговой сети электроники.

Этот модуль содержит модели, представляющие иерархическую структуру
торговой сети: заводы, розничные сети и индивидуальных предпринимателей.
"""

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class NetworkNode(models.Model):
    """
    Модель звена торговой сети электроники.

    Представляет собой узел в иерархической структуре сети, который может быть:
    - Заводом (уровень 0) - не имеет поставщика
    - Розничной сетью (уровень 1 или выше) - закупает у завода или другой сети
    - Индивидуальным предпринимателем (уровень 1 или выше) - закупает у кого-либо

    Уровень иерархии определяется автоматически на основе поставщика:
    - Если поставщика нет - уровень 0 (завод)
    - Если поставщик уровня 0 - уровень 1
    - Если поставщик уровня N - уровень N+1
    """

    # ТИПЫ ЗВЕНЬЕВ СЕТИ
    # Используем TextChoices для удобного представления типов в админке и API
    class NodeType(models.TextChoices):
        FACTORY = 'FACTORY', _('Завод')  # Производитель электроники
        RETAIL_NETWORK = 'RETAIL', _('Розничная сеть')  # Сеть магазинов
        ENTREPRENEUR = 'IE', _('Индивидуальный предприниматель')  # ИП

    # ОСНОВНАЯ ИНФОРМАЦИЯ
    # ===================

    name = models.CharField(
        max_length=255,
        verbose_name=_('Название'),
        help_text=_('Название организации (например, "Завод электроники Самсунг")')
    )

    node_type = models.CharField(
        max_length=10,
        choices=NodeType.choices,
        default=NodeType.FACTORY,
        verbose_name=_('Тип звена'),
        help_text=_('Тип организации в цепи поставок')
    )

    # КОНТАКТНАЯ ИНФОРМАЦИЯ
    # =====================

    email = models.EmailField(
        verbose_name=_('Email'),
        help_text=_('Контактный email организации')
    )

    country = models.CharField(
        max_length=100,
        verbose_name=_('Страна'),
        help_text=_('Страна регистрации организации')
    )

    city = models.CharField(
        max_length=100,
        verbose_name=_('Город'),
        help_text=_('Город нахождения организации'),
        db_index=True  # Добавляем индекс для быстрой фильтрации по городу
    )

    street = models.CharField(
        max_length=255,
        verbose_name=_('Улица'),
        help_text=_('Название улицы')
    )

    house_number = models.CharField(
        max_length=20,
        verbose_name=_('Номер дома'),
        help_text=_('Номер дома, может включать корпус и строение')
    )

    # ИЕРАРХИЧЕСКАЯ СТРУКТУРА
    # =======================

    supplier = models.ForeignKey(
        'self',  # Ссылка на эту же модель - создает иерархию
        on_delete=models.PROTECT,  # PROTECT запрещает удаление, если есть зависимые
        null=True,  # NULL означает, что это завод (верхний уровень)
        blank=True,
        related_name='clients',  # Обратная связь: supplier.clients.all()
        verbose_name=_('Поставщик'),
        help_text=_('Поставщик продукции (пусто для заводов)')
    )

    hierarchy_level = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_('Уровень иерархии'),
        help_text=_('0 - завод, 1 - прямой клиент завода, и т.д.'),
        editable=False  # Это поле рассчитывается автоматически
    )

    # ФИНАНСОВАЯ ИНФОРМАЦИЯ
    # =====================

    debt = models.DecimalField(
        max_digits=15,  # Максимум 15 цифр всего
        decimal_places=2,  # Из них 2 знака после запятой (копейки)
        default=0.00,
        validators=[MinValueValidator(0.00)],  # Долг не может быть отрицательным
        verbose_name=_('Задолженность перед поставщиком'),
        help_text=_('Сумма задолженности в рублях (с копейками)')
    )

    # ВРЕМЕННЫЕ МЕТКИ
    # ===============

    created_at = models.DateTimeField(
        auto_now_add=True,  # Автоматически устанавливается при создании
        verbose_name=_('Дата создания'),
        help_text=_('Дата и время создания записи в системе')
    )

    updated_at = models.DateTimeField(
        auto_now=True,  # Автоматически обновляется при каждом сохранении
        verbose_name=_('Дата обновления'),
        help_text=_('Дата и время последнего обновления записи')
    )

    class Meta:
        """
        Метаданные модели - настройки отображения и поведения.
        """
        verbose_name = _('Звено сети')
        verbose_name_plural = _('Звенья сети')
        ordering = ['hierarchy_level', 'name']  # Сортировка: сначала по уровню, потом по имени
        indexes = [
            # Составной индекс для быстрого поиска по стране и уровню
            models.Index(fields=['country', 'hierarchy_level']),
            # Индекс для фильтрации по поставщику и типу
            models.Index(fields=['supplier', 'node_type']),
        ]

    def __str__(self):
        """
        Строковое представление объекта - отображается в админке и при печати.

        Возвращает строку вида: "Завод Samsung (уровень 0)"
        """
        return f"{self.name} (уровень {self.hierarchy_level})"

    def save(self, *args, **kwargs):
        """
        Переопределяем метод сохранения для автоматического расчета уровня иерархии.

        Этот метод вызывается каждый раз при сохранении объекта в БД.
        Мы используем его, чтобы автоматически вычислить уровень иерархии
        на основе поставщика.
        """
        # Рассчитываем уровень иерархии
        if self.supplier is None:
            # Нет поставщика = завод = уровень 0
            self.hierarchy_level = 0
        else:
            # Уровень = уровень поставщика + 1
            # Например, если поставщик уровня 0, то мы уровня 1
            self.hierarchy_level = self.supplier.hierarchy_level + 1

        # Вызываем оригинальный метод save для фактического сохранения
        super().save(*args, **kwargs)

    def get_full_address(self):
        """
        Возвращает полный адрес в читаемом формате.

        Returns:
            str: Адрес в формате "Страна, Город, Улица, дом Номер"
        """
        return f"{self.country}, {self.city}, {self.street}, дом {self.house_number}"

    def clear_debt(self):
        """
        Очищает задолженность перед поставщиком.

        Этот метод используется в admin action для массового обнуления долгов.
        """
        self.debt = 0.00
        self.save(update_fields=['debt', 'updated_at'])


class Product(models.Model):
    """
    Модель продукта (товара) в торговой сети.

    Представляет конкретный продукт электроники, который продается
    или производится звеном сети.
    """

    network_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,  # При удалении узла удаляются и его продукты
        related_name='products',  # Доступ: network_node.products.all()
        verbose_name=_('Звено сети'),
        help_text=_('К какому звену сети относится этот продукт')
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_('Название продукта'),
        help_text=_('Название продукта (например, "Смартфон")')
    )

    model = models.CharField(
        max_length=100,
        verbose_name=_('Модель'),
        help_text=_('Модель продукта (например, "Galaxy S21")')
    )

    release_date = models.DateField(
        verbose_name=_('Дата выхода на рынок'),
        help_text=_('Дата, когда продукт появился на рынке')
    )

    class Meta:
        """
        Метаданные модели продукта.
        """
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')
        ordering = ['-release_date', 'name']  # Сначала новые, потом по алфавиту
        # Уникальность: один узел не может иметь два одинаковых продукта с одной моделью
        unique_together = [['network_node', 'name', 'model']]

    def __str__(self):
        """
        Строковое представление продукта.

        Возвращает: "Название Модель (Дата выхода)"
        """
        return f"{self.name} {self.model} ({self.release_date})"