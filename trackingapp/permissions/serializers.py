from rest_framework import serializers
from .models import Role, Permission
from django.db import connection, reset_queries
from user.models import User
from base.serializers import BulkDeleteSerializer
from functools import reduce
import uuid

class PermissionSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only= True)
    
    class Meta:
        model = Permission
        fields = ['code_name', 'friendly_name', 'id']


class BulkDetelePermissionSerializer(BulkDeleteSerializer):

    class Meta:
        model = Permission
        fields = ['ids']

class GetRoleSerializer(serializers.ModelSerializer):

    permission = PermissionSerializer(many = True, read_only= True)
    
    class Meta:
        model = Role
        fields = ['id', 'code_name', 'friendly_name', 'permission']
        

class WriteRoleSerializer(serializers.ModelSerializer):
    
    permission = serializers.PrimaryKeyRelatedField(many = True, required= False, queryset = Permission.objects.all())

    class Meta:
        model = Role
        fields = ['code_name', 'friendly_name', 'permission']

    def validate_permission(self, permission):
        error_ids = []
        permission_set = set()
        for perm in permission:
            if perm in permission_set:
                error_ids.append(
                    f'permission {perm.friendly_name} - id {perm.id} duplicate')
            permission_set.add(perm)
        if self.instance:
            permission_old_ids = self.instance.permission.all().values_list('id', flat=True)

            error_ids = error_ids + reduce(lambda prev, curr: prev + [
                                           f'Permission {perm.friendly_name} - id {curr.id} have already exisited.']
                                           if curr.id in permission_old_ids else prev, permission_set, [])
        if error_ids:
            raise serializers.ValidationError(error_ids)
        return permission


class UpdatePermissionOfRoleSerializer(serializers.ModelSerializer):
    
    permission = serializers.PrimaryKeyRelatedField(queryset = Permission.objects.all(), many = True, write_only= True)
    permission_name = serializers.StringRelatedField(many = True,read_only= True)
    
    class Meta:
        model = Role 
        fields = ['permission', 'permission_name']
    
    def update(self, instance, data):
        if self.context.get('view').action == "add_permission":
            data['permission'] = reduce(
                lambda prev, curr: prev + [curr], instance.permission.all(), data['permission'])
        elif self.context.get('view').action == "delete_permission":
            data['permission'] = reduce(lambda prev, curr: prev + [
                                        curr] if curr not in data['permission'] else prev, instance.permission.all(), [])
        return super().update(instance, data)


class BulkDeteleRoleSerializer(BulkDeleteSerializer):

    class Meta:
        model = Role
        fields = ['ids']
