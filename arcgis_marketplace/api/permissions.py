from rest_framework import permissions


class Signed(permissions.BasePermission):

    def has_permission(self, request, view):
        return hasattr(request.user, 'account')


class IsStaffList(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list' and request.user is not None:
            return request.user.is_staff
        return True


class IsStaffOrSelf(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user == obj.user


class OwnItem(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or\
                not hasattr(obj, 'owner'):
            return True

        return obj.owner.user == request.user


class ReadOnlyOrSigned(Signed):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_permission(request, view)
