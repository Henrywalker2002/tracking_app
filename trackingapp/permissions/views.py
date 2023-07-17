from base.views import BulkActionBaseModelViewSet
from permissions.serializers import (WriteRoleSerializer, GetRoleSerializer, WritePermissionSerializer,
                          GetPermissionSerializer, BulkDeteleRoleSerializer, BulkDetelePermissionSerializer, UpdatePermissionOfRoleSerializer)
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
                        "bulk_delete": BulkDeteleRoleSerializer, 'add_permission' : UpdatePermissionOfRoleSerializer, 
                        "delete_permission" : UpdatePermissionOfRoleSerializer , "default": GetRoleSerializer}

    queryset = Role.objects.all()
    permission_classes = [CustomPermission]

    @action(detail=True, url_path='view-permission')
    def view_permission(self, request, pk):
        instance = self.get_object()
        permission_lst = instance.permission.all()
        serializer = GetPermissionSerializer(permission_lst, many = True)
        return Response(serializer.data)

    @action(detail= True, url_path= 'add-permission', methods= ['patch'])
    def add_permission(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail= True, url_path='delete-permission', methods= ['patch'])
    def delete_permission(self, request, pk):
        return self.add_permission(request, pk)
        
class PermissionModelViewSet(BulkActionBaseModelViewSet):

    serializer_class = {"create": WritePermissionSerializer, "update": WritePermissionSerializer, "partial_update": WritePermissionSerializer,
                        "bulk_delete": WritePermissionSerializer, "default": GetPermissionSerializer}
    
    queryset = Permission.objects.all()
    permission_classes = [CustomPermission]
