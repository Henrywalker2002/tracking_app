from base.views import BulkActionBaseModelViewSet
from permissions.serializers.role import (WriteRoleSerializer, ReadRoleDetailSerializer, 
                                     ReadRoleSummarySerializer, BulkDeteleRoleSerializer, UpdatePermissionOfRoleSerializer)
from permissions.serializers.permission import (PermissionSerializer, BulkDetelePermissionSerializer, ReadPermissionSerializer)
from .models import Role, Permission
from rest_framework import permissions, status
from rest_framework.response import Response
from django.db import connection, reset_queries
from permissions.custom_permission import RolePermission
from rest_framework.decorators import action
import logging
from functools import reduce
from base.decorators import query_debugger

class RoleModelViewSet(BulkActionBaseModelViewSet):

    serializer_class = {"create": WriteRoleSerializer, "update": WriteRoleSerializer, "partial_update": WriteRoleSerializer,
                        "bulk_delete": BulkDeteleRoleSerializer, 'add_permission' : UpdatePermissionOfRoleSerializer, 
                        "delete_permission" : UpdatePermissionOfRoleSerializer , "default": ReadRoleSummarySerializer, 
                        "retrieve" : ReadRoleDetailSerializer, "list" : ReadRoleDetailSerializer}

    queryset = Role.objects.all()
    permission_classes = [RolePermission]
    search_fields = ['friendly_name', 'code_name']
    filterset_fields = ['code_name', 'created_by']
    
    def get_queryset(self):
        if self.action == "list":
            return self.queryset.prefetch_related('permission')
        return super().get_queryset()
    

    @action(detail= True, url_path= 'add-permission', methods= ['patch'])
    def add_permission(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        serializer_return = self.get_serializer(instance, is_get = True)
        return Response(serializer_return.data)
    
    @action(detail= True, url_path='delete-permission', methods= ['patch'])
    def delete_permission(self, request, pk):
        return self.add_permission(request, pk)
        
class PermissionModelViewSet(BulkActionBaseModelViewSet):

    serializer_class = {"bulk_delete": BulkDetelePermissionSerializer, "default": PermissionSerializer, 
                        "retrieve" : ReadPermissionSerializer, "list" : ReadPermissionSerializer}
    
    queryset = Permission.objects.all()
    permission_classes = [RolePermission]
    search_fields = ['friendly_name', 'code_name']
    filterset_fields = ['code_name']
