"""
Кастомные права доступа для API торговой сети.

Этот модуль определяет права доступа для различных операций с API.
Согласно ТЗ: только активные сотрудники имеют доступ к API.
"""

from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    """
    Право доступа: только для активных сотрудников.

    ТРЕБОВАНИЕ ТЗ: "Настроить права доступа к API так, чтобы только
    активные сотрудники имели доступ к API."

    Проверяет два условия:
    1. Пользователь аутентифицирован (залогинен)
    2. Пользователь активен (is_active = True)
    """

    message = 'Доступ разрешен только активным сотрудникам.'

    def has_permission(self, request, view):
        """
        Проверяет, имеет ли пользователь доступ к view.

        Args:
            request: HTTP запрос
            view: View, к которому запрашивается доступ

        Returns:
            bool: True если доступ разрешен, False иначе
        """
        # Проверяем, что пользователь аутентифицирован И активен
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active
        )

    def has_object_permission(self, request, view, obj):
        """
        Проверяет, имеет ли пользователь доступ к конкретному объекту.

        Args:
            request: HTTP запрос
            view: View
            obj: Конкретный объект модели

        Returns:
            bool: True если доступ разрешен, False иначе
        """
        # Используем ту же логику для объектов
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active
        )


class IsActiveEmployeeOrReadOnly(permissions.BasePermission):
    """
    Право доступа: чтение для всех, изменение только для активных сотрудников.

    Это более гибкое право, которое можно использовать если нужно
    разрешить публичный просмотр данных, но изменение только сотрудникам.
    """

    message = 'Изменение данных разрешено только активным сотрудникам.'

    def has_permission(self, request, view):
        """
        Проверяет доступ на уровне view.

        Безопасные методы (GET, HEAD, OPTIONS) доступны всем.
        Остальные методы (POST, PUT, PATCH, DELETE) - только активным сотрудникам.

        Args:
            request: HTTP запрос
            view: View

        Returns:
            bool: True если доступ разрешен, False иначе
        """
        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для небезопасных методов требуем активного сотрудника
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Право доступа: чтение для активных сотрудников, изменение только для админов.

    Полезно для защиты критичных данных, которые должны редактировать
    только администраторы.
    """

    message = 'Изменение данных разрешено только администраторам.'

    def has_permission(self, request, view):
        """
        Проверяет доступ на уровне view.

        Args:
            request: HTTP запрос
            view: View

        Returns:
            bool: True если доступ разрешен, False иначе
        """
        # Для безопасных методов требуем активного сотрудника
        if request.method in permissions.SAFE_METHODS:
            return bool(
                request.user and
                request.user.is_authenticated and
                request.user.is_active
            )

        # Для небезопасных методов требуем права администратора
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active and
            request.user.is_staff
        )