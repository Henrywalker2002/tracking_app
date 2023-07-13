from base.views import BulkActionBaseModelViewSet
from permissions.serializers import (WriteRoleSerializer, GetRoleSerializer, WritePermissionSerializer,
                          GetPermissionSerializer, BulkDeteleRoleSerializer, BulkDetelePermissionSerializer)
from .models import Role, Permission
from rest_framework import permissions
from rest_framework.response import Response
from django.db import connection, reset_queries
from base.permission import CustomPermission
from rest_framework.decorators import action
import logging
from functools import reduce

class RoleModelViewSet(BulkActionBaseModelViewSet):

    serializer_class = {"create": WriteRoleSerializer, "update": WriteRoleSerializer, "partial_update": WriteRoleSerializer,
                        "bulk_delete": BulkDeteleRoleSerializer, "default": GetRoleSerializer}

    queryset = Role.objects.all()
    permission_classes = [CustomPermission]

    @action(detail=True, url_path='view-permission')
    def view_permission(self, request):
        permission_lst = self.instance.permission.all()
        lst = []
        for per in permission_lst:
            lst.append(per.code_name)
        return Response(lst)


class PermissionModelViewSet(BulkActionBaseModelViewSet):

    serializer_class = {"create": WritePermissionSerializer, "update": WritePermissionSerializer, "partial_update": WritePermissionSerializer,
                        "bulk_delete": WritePermissionSerializer, "default": GetPermissionSerializer}
    
    queryset = Permission.objects.all()
    permission_classes = [CustomPermission]
