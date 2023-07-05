import re
from django.db.models import fields
from rest_framework import serializers
from .models import User
from permissions.models import Role
from django.db import transaction
from functools import reduce
import logging
from trackingapp.custom_middleware import get_current_request_id
from base.serializers import BulkUpdateSerializer

class WriteUserModelSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password',
                  'first_name', 'last_name', 'created_at', 'modified_at', 'phone', 'role_names']

    def validate_phone(self, phone):
        regex_phone = "^(0|\+84)\d{9}$"
        if not re.match(regex_phone, phone):
            raise serializers.ValidationError("wrong format phone number")
        return phone
    
    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError('password must have at least 8 characters')
        return password
    
class UpdateRolesSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(read_only= True)
    
    class Meta :
        model = User 
        fields = ['id', 'email' , 'roles', 'role_names']
        extra_kwargs = {"roles" : {"write_only" : True}}

    def validate_roles(self, roles):
        error_ids = []
        roles_set = set()
        for role in roles :
            if role in roles_set:
                error_ids.append(f'Role {role.code_name} - id {role.id} duplicate')
            roles_set.add(role)
        if self.instance:
            old_roles_ids = self.instance.roles.all().values_list('id', flat=True)

            error_ids = error_ids + reduce(lambda prev, curr: prev + [
                f'Role {role.friendly_name} - id: {curr.id} have already exisited.'] if curr.id in old_roles_ids else prev, roles_set, [])
        if error_ids:
            raise serializers.ValidationError(error_ids)
        return roles

    def update(self, instance, data):
        if 'roles' in data.keys():
            data['roles'] = reduce(lambda prev, curr : prev + [curr], instance.roles.all(), data['roles'])
        instance = super().update(instance, data)
        return instance

class DeleteRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'roles')
    
    def validate_roles(self, roles):
        error_ids = []
        roles_set = set()
        for role in roles :
            if role in roles_set:
                error_ids.append(f'Role {role.friendly_name} - id {role.id} duplicate')
            roles_set.add(role)
        if error_ids:
            raise serializers.ValidationError(error_ids)
        if self.instance:
            old_roles_ids = self.instance.roles.all().values_list('id', flat=True)
            
        error_ids = error_ids + reduce(lambda prev, curr: prev + [
            f'Role {role.friendly_name} - id {curr.id} have not exisited.'] if curr.id not in old_roles_ids else prev, roles_set, [])
        if error_ids:
            raise serializers.ValidationError(error_ids)
        return roles

class GetUserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'full_name', 'phone', "role_names"]

class BulkUpdateUserSerializer(BulkUpdateSerializer):
    
    password = serializers.CharField(write_only= True)
    
    class Meta: 
        model = User
        fields = '__all__' 

class LoginSerializer(serializers.Serializer):
    
    id = serializers.ReadOnlyField()
    email = serializers.EmailField(max_length=128)
    password = serializers.CharField(max_length=128, write_only=True)
    first_name = serializers.CharField(max_length = 128, read_only= True)
    last_name = serializers.CharField(max_length = 128, read_only= True)
    phone = serializers.CharField(max_length = 12, read_only= True)
    full_name = serializers.ReadOnlyField()
    permission_code_names = serializers.ReadOnlyField()
    role_names = serializers.ReadOnlyField()
    
    class Meta:
        Model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'phone', 'permission_code_names', 'role_names']
        
