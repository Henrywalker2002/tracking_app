import re
from django.db.models import fields
from rest_framework import serializers
from .models import User
from permissions.models import Role
from django.db import transaction


class PostUserModelSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    role_ids = serializers.ListField(child = serializers.UUIDField(), required= False)

    class Meta:
        model = User
        fields = ['id', 'email', 'password',
                  'first_name', 'last_name', 'phone', 'role_ids']

    @transaction.atomic()
    def create(self, validated_data):
        role_ids = validated_data.pop('role_ids')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        roles = Role.objects.filter(id__in = role_ids)
        for role in roles : 
            role.user.add(user)
            role.save()
        return user

    def validate_phone(self, phone):
        regex_phone = "^(0|\+84)\d{9}$"
        if not re.match(regex_phone, phone):
            raise serializers.ValidationError("wrong format phone number")
        return phone
    
    def validate_role_ids(self, role_ids):
        return role_ids


class GetUserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'full_name', 'phone']

class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField(max_length = 128, write_only = True)
    password = serializers.CharField(max_length = 128, write_only= True)
    