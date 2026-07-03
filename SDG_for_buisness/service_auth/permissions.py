from rest_framework.permissions import BasePermission


class HasScope(BasePermission):

    def has_permission(self, request, view):
        required_scope = getattr(view, "required_scope", None)

        if not required_scope:
            return True

        service = request.user

        return (
            hasattr(service, "has_scope")
            and service.has_scope(required_scope)
        )

