from rest_framework import serializers
from permissions.models import Role, Permission
from user.models import User
from base.serializers import BulkDeleteSerializer
from functools import reduce
import uuid

class ReadSortUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name'] 

class ReadPermissionSerializer(serializers.ModelSerializer):
    
    created_by = ReadSortUserSerializer(read_only= True)
    updated_by = ReadSortUserSerializer(read_only= True)
    
    class Meta:
        model = Permission
        fields = ['id', 'code_name', 'friendly_name', 'created_at', 'modified_at', 'created_by', 'updated_by']

class PermissionSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only= True)
    
    class Meta:
        model = Permission
        fields = ['code_name', 'friendly_name', 'id']


class BulkDetelePermissionSerializer(BulkDeleteSerializer):

    class Meta:
        model = Permission
        fields = ['ids']

