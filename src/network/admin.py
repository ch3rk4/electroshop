"""
Конфигурация админ-панели для торговой сети.

Этот модуль настраивает интерфейс Django Admin для удобного управления
звеньями сети и продуктами.
"""

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import NetworkNode, Product


class ProductInline(admin.TabularInline):
    """
    Inline для отображения продуктов прямо на странице звена сети.

    TabularInline отображает продукты в виде таблицы,
    что позволяет редактировать несколько продуктов одновременно
    не покидая страницу редактирования звена сети.
    """
    model = Product
    extra = 1  # Показывать одну пустую форму для добавления нового продукта
    fields = ('name', 'model', 'release_date')  # Поля для отображения

    # Настройка автозаполнения для удобства работы с большими списками
    autocomplete_fields = []


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """
    Настройка админ-панели для модели NetworkNode (звено сети).

    Этот класс определяет, как звенья сети отображаются и редактируются
    в Django админ-панели. Мы добавляем фильтры, поиск, ссылки и
    специальные действия согласно требованиям ТЗ.
    """

    # ОТОБРАЖЕНИЕ СПИСКА ОБЪЕКТОВ
    # ============================

    list_display = (
        'name',  # Название звена
        'node_type',  # Тип (завод/сеть/ИП)
        'city',  # Город
        'hierarchy_level',  # Уровень в иерархии
        'supplier_link',  # Кликабельная ссылка на поставщика (кастомное поле)
        'debt',  # Задолженность
        'created_at',  # Дата создания
    )

    # Поля, которые можно редактировать прямо из списка (без перехода на страницу)
    list_editable = []  # Долг намеренно НЕ редактируемый через список

    # Поля, по которым можно кликнуть для перехода к детальной странице
    list_display_links = ('name',)

    # ФИЛЬТРАЦИЯ
    # ==========

    # Боковая панель с фильтрами - позволяет быстро найти нужные объекты
    list_filter = (
        'node_type',  # Фильтр по типу звена
        'city',  # Фильтр по городу (ТРЕБОВАНИЕ ТЗ)
        'hierarchy_level',  # Фильтр по уровню иерархии
        'country',  # Фильтр по стране
    )

    # ПОИСК
    # =====

    # Поля, по которым работает поиск в админке
    search_fields = (
        'name',  # Поиск по названию
        'email',  # Поиск по email
        'city',  # Поиск по городу
        'country',  # Поиск по стране
    )

    # ОРГАНИЗАЦИЯ ПОЛЕЙ НА СТРАНИЦЕ РЕДАКТИРОВАНИЯ
    # =============================================

    # Группируем поля по разделам для удобства
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('name', 'node_type')
        }),
        (_('Контактная информация'), {
            'fields': ('email', 'country', 'city', 'street', 'house_number')
        }),
        (_('Иерархия и финансы'), {
            'fields': ('supplier', 'debt'),
            'description': _('Поставщик определяет уровень в иерархии. '
                             'Долг можно изменить только через API или admin action.')
        }),
        (_('Системная информация'), {
            'fields': ('hierarchy_level', 'created_at', 'updated_at'),
            'classes': ('collapse',),  # Этот раздел свернут по умолчанию
        }),
    )

    # Поля только для чтения (их можно видеть, но нельзя редактировать)
    readonly_fields = (
        'hierarchy_level',  # Рассчитывается автоматически
        'created_at',  # Устанавливается при создании
        'updated_at',  # Обновляется автоматически
    )

    # INLINE МОДЕЛИ
    # =============

    # Отображаем продукты прямо на странице звена сети
    inlines = [ProductInline]

    # ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ
    # ========================

    # Количество объектов на странице списка
    list_per_page = 25

    # Сохранить кнопки "Сохранить" вверху страницы редактирования
    save_on_top = True

    # Поля для автозаполнения (улучшает производительность с большими списками)
    autocomplete_fields = ['supplier']

    # КАСТОМНЫЕ МЕТОДЫ ДЛЯ ОТОБРАЖЕНИЯ
    # ================================

    @admin.display(description=_('Поставщик'), ordering='supplier__name')
    def supplier_link(self, obj: NetworkNode) -> str:
        """
        Создает кликабельную ссылку на поставщика (ТРЕБОВАНИЕ ТЗ).

        Этот метод генерирует HTML-ссылку, которая ведет на страницу
        редактирования поставщика. Если поставщика нет (завод),
        отображается прочерк.

        Args:
            obj: Объект NetworkNode, для которого создаем ссылку

        Returns:
            HTML-строка со ссылкой или прочерком
        """
        if obj.supplier:
            # Получаем URL админки для редактирования поставщика
            url = reverse('admin:network_networknode_change', args=[obj.supplier.pk])
            # Создаем HTML-ссылку с именем поставщика
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return '—'  # Прочерк, если поставщика нет

    # ADMIN ACTIONS
    # =============

    @admin.action(description=_('Очистить задолженность перед поставщиком'))
    def clear_debt(self, request: HttpRequest, queryset: QuerySet) -> None:
        """
        Admin action для массовой очистки задолженности (ТРЕБОВАНИЕ ТЗ).

        Это действие позволяет администратору выбрать несколько звеньев сети
        в списке и одним кликом обнулить их задолженность перед поставщиками.
        После выполнения показывается сообщение об успехе.

        Args:
            request: HTTP запрос
            queryset: QuerySet выбранных объектов
        """
        # Обновляем все выбранные объекты одним SQL-запросом (эффективно!)
        updated_count = queryset.update(debt=0.00)

        # Показываем сообщение об успехе
        # Используем правильное склонение для русского языка
        if updated_count == 1:
            message = _('Задолженность очищена для 1 звена сети.')
        else:
            message = _(f'Задолженность очищена для {updated_count} звеньев сети.')

        self.message_user(request, message)

    # Регистрируем наше действие
    actions = ['clear_debt']

    # ПЕРЕОПРЕДЕЛЕНИЕ МЕТОДОВ
    # =======================

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """
        Оптимизируем запросы к БД.

        Используем select_related для загрузки связанных поставщиков
        одним запросом вместо N+1 запросов. Это значительно ускоряет
        загрузку списка звеньев сети в админке.

        Args:
            request: HTTP запрос

        Returns:
            Оптимизированный QuerySet
        """
        queryset = super().get_queryset(request)
        # select_related загружает связанного поставщика сразу
        return queryset.select_related('supplier')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Настройка админ-панели для модели Product (продукт).

    Более простая конфигурация для управления продуктами.
    """

    # ОТОБРАЖЕНИЕ СПИСКА
    # ==================

    list_display = (
        'name',
        'model',
        'network_node',
        'release_date',
    )

    # ФИЛЬТРАЦИЯ И ПОИСК
    # ==================

    list_filter = (
        'release_date',
        'network_node__node_type',  # Фильтр по типу звена (через связь)
    )

    search_fields = (
        'name',
        'model',
        'network_node__name',  # Поиск по названию звена
    )

    # ОРГАНИЗАЦИЯ ПОЛЕЙ
    # =================

    fields = (
        'network_node',
        'name',
        'model',
        'release_date',
    )

    # Автозаполнение для выбора звена сети
    autocomplete_fields = ['network_node']

    # Сортировка по умолчанию
    ordering = ('-release_date', 'name')

    # Количество объектов на странице
    list_per_page = 50

    # Фильтры справа от списка (экономит место)
    list_filter_position = 'right'