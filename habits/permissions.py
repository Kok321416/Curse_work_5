from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет только владельцам объекта редактировать его.
    Предполагает, что экземпляр модели имеет атрибут `user`.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешения на чтение предоставляются для любого запроса,
        # поэтому мы всегда разрешаем GET, HEAD или OPTIONS запросы.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешения на запись предоставляются только владельцу объекта.
        return obj.user == request.user


class IsOwner(permissions.BasePermission):
    """
    Разрешение, которое позволяет доступ только владельцам объекта.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
