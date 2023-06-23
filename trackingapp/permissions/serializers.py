from rest_framework import serializers
from .models import Role, Permission
from django.db import connection, reset_queries
from user.models import User
from baseapp.serializers import AutoAddCreateBySerializer, BulkSerializer
from functools import reduce


class PostRoleSerializer(AutoAddCreateBySerializer):

    class Meta:
        model = Role
        fields = ['id', 'created_by', 'updated_by',
                  'friendly_name', 'code_name', 'permission']

    def validate_permission(self, permission):
        error_ids = []
        permission_set = set()
        for perm in permission:
            if perm in permission_set:
                error_ids.append(f'Role id {perm.id} duplicate')
            permission_set.add(perm)
        if self.instance:
            permission_old_ids = self.instance.permission.all().values_list('id', flat=True)

            error_ids = error_ids + reduce(lambda prev, curr: prev + [
                                           f'Permission id {curr.id} have already exisited.'] 
                                           if curr.id in permission_old_ids else prev, permission_set, [])
        if error_ids:
            raise serializers.ValidationError(error_ids)
        return permission
    
    def update(self, instance, data):
        if 'permission' in data.keys():
            data['permission'] = reduce(lambda prev, curr : prev + [curr], instance.permission.all(), data['permission'])
        return super().update(instance, data)

class GetRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'


class BulkDeteleRoleSerializer(BulkSerializer):

    class Meta:
        model = Role
        fields = ['ids']


class PostPermissionSerializer(AutoAddCreateBySerializer):

    class Meta:
        model = Permission
        fields = '__all__'
        extra_kwargs = {"role": {"required": False}}


class GetPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'


class BulkDetelePermissionSerializer(BulkSerializer):

    class Meta:
        model = Permission
        fields = ['ids']
