import re
from django.db.models import fields
from rest_framework import serializers
from .models import User
from permissions.models import Role
from django.db import transaction
from functools import reduce
import logging
from trackingapp.custom_middleware import get_current_request_id


class PostUserModelSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password',
                  'first_name', 'last_name', 'phone', 'roles']
        extra_kwargs = {"roles": {"required": False}}

    def validate_roles(self, roles):
        error_ids = []
        roles_set = set()
        for role in roles :
            if role in roles_set:
                error_ids.append(f'Role id {role.id} duplicate')
            roles_set.add(role)
        if self.instance:
            old_roles_ids = self.instance.roles.all().values_list('id', flat=True)

            error_ids = error_ids + reduce(lambda prev, curr: prev + [
                            f'Role id {curr.id} have already exisited.'] if curr.id in old_roles_ids else prev, roles_set, [])
        if error_ids:
            raise serializers.ValidationError(error_ids)
        return roles

    def update(self, instance, data):
        if 'roles' in data.keys():
            data['roles'] = reduce(lambda prev, curr : prev + [curr], instance.roles.all(), data['roles'])
        instance = super().update(instance, data)
        return instance

    def validate_phone(self, phone):
        regex_phone = "^(0|\+84)\d{9}$"
        if not re.match(regex_phone, phone):
            raise serializers.ValidationError("wrong format phone number")
        return phone


class GetUserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'full_name', 'phone', "roles"]


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=128, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
