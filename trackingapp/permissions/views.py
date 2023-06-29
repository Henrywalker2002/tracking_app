from base.views import CustomModelViewSetBase

from .serializers import (WriteRoleSerializer, GetRoleSerializer, WritePermissionSerializer, BulkUpdatePermissionSerializer,
                          GetPermissionSerializer, BulkDeteleRoleSerializer, BulkDetelePermissionSerializer)
from .models import Role, Permission
from rest_framework import permissions
from rest_framework.response import Response
from django.db import connection, reset_queries
from base.permission import CustomPermission
from rest_framework.decorators import action
import logging
from functools import reduce

class RoleModelViewSet(CustomModelViewSetBase):

    serializer_class = {"create": WriteRoleSerializer, "update": WriteRoleSerializer, "partial_update": WriteRoleSerializer,
                        "bulk_update": WriteRoleSerializer, "bulk_delete": BulkDeteleRoleSerializer, "default": GetRoleSerializer}

    queryset = Role.objects.all()
    permission_classes = [CustomPermission]

    @action(detail=True, url_path='view-permission')
    def view_permission(self, request):
        permission_lst = self.instance.permission.all()
        lst = []
        for per in permission_lst:
            lst.append(per.code_name)
        return Response(lst)


class PermissionModelViewSet(CustomModelViewSetBase):

    serializer_class = {"create": WritePermissionSerializer, "update": WritePermissionSerializer, "partial_update": WritePermissionSerializer,
                        "bulk_delete": WritePermissionSerializer, "bulk_update": BulkUpdatePermissionSerializer, "default": GetPermissionSerializer}
    
    queryset = Permission.objects.all()
    permission_classes = [CustomPermission]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
