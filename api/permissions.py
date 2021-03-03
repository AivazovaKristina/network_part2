from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return request.user.is_admin

        return False


class IsModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return request.user.is_moderator
        return False


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class MyCustomPermissionClass(permissions.BasePermission):
    # def is_authenticated(self, request):
        # return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action == 'create' and request.user.is_authenticated:
            return True
        if request.user.is_authenticated and (view.action == 'destroy' or view.action == 'update' or view.action == 'partial_update') and (request.user.is_admin or request.user.is_moderator or (request.user == obj.author and request.user.is_user)):
            return True
        if view.action == 'list' or view.action == 'retrieve':
            return True
        return False