from baseapp.views import CustomModelViewSetBase
from .serializers import (PostRoleSerializer, GetRoleSerializer, PostPermissionSerializer, 
                GetPermissionSerializer, BulkDeteleRoleSerializer, BulkDetelePermissionSerializer)
from .models import Role, Permission
from rest_framework import permissions
from rest_framework.response import Response
from django.db import connection, reset_queries
from baseapp.permission import CustomPermission

import logging


class RoleModelViewSet(CustomModelViewSetBase):

    serializer_class = {"create": PostRoleSerializer, "update": PostRoleSerializer,
                        "bulk_update": PostRoleSerializer, "bulk_delete": BulkDeteleRoleSerializer, "default": GetRoleSerializer}
    queryset = Role.objects.all()
    permission_classes = [CustomPermission]


class PermissionModelViewSet(CustomModelViewSetBase):
    serializer_class = {"create": PostPermissionSerializer, "update": PostPermissionSerializer,
                        "bulk_delete": BulkDetelePermissionSerializer, "default": GetPermissionSerializer}
    queryset = Permission.objects.all()
    permission_classes = [CustomPermission]
