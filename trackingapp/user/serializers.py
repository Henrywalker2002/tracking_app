import re
from django.db.models import fields
from rest_framework import serializers
from .models import User
from permissions.models import Role
from django.db import transaction
from functools import reduce
import logging
from trackingapp.custom_middleware import get_current_request_id 
from permissions.serializers.role import ReadRoleSummarySerializer


class CreateUserModelSerializer(serializers.ModelSerializer):

    roles = serializers.PrimaryKeyRelatedField(required= False, queryset = Role.objects.all(), many = True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'roles', 'is_active']
 
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

class ReadUserSummarySerializer(serializers.ModelSerializer):

    roles = serializers.SlugRelatedField(slug_field= 'friendly_name', read_only= True, many = True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'full_name', 'phone', "roles", "is_active"]
        
class ReadUserDetailSerializer(ReadUserSummarySerializer):
    
    roles = ReadRoleSummarySerializer(many= True, read_only= True)
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['permission'] = permission_code_names = reduce(lambda prev, curr: prev | set(
                    curr.permission.all().values_list('code_name', flat=True)), instance.roles.all(), set())
        return ret

class ReadSortUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']    

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
        
class UpdateUserSerializer(CreateUserModelSerializer):
    email = serializers.EmailField(read_only= True)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, email):
        instance = User.objects.filter(email = email)
        if not instance:
            raise serializers.ValidationError(f"account with email {email} doesn't exist")
        return email

class ResetPassword(ForgotPasswordSerializer):
    # inherit to get email fields 
    code = serializers.CharField()
    password = serializers.CharField()
    
    def validate_code(self, code):
        if len(code) != 6:
            raise serializers.ValidationError("code is not valid")
        return code
    
    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError('password must have at least 8 characters')
        return password