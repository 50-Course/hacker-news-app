from __future__ import annotations

from rest_framework.permissions import BasePermission


class was_created_internally(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.was_created_internally)
