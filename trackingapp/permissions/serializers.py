from rest_framework import serializers
from .models import Role, Permission
from django.db import connection, reset_queries
from user.models import User
from baseapp.serializers import AutoAddCreateBySerializer, BulkSerializer


class PostRoleSerializer(AutoAddCreateBySerializer):

    class Meta:
        model = Role
        fields = ['id', 'created_by', 'updated_by',
                  'friendly_name', 'code_name', 'user']
        extra_kwargs = {"user": {"required": False}}

    # def create(self, data):
    #     reset_queries()
    #     users = data.pop('user')
    #     instance = self.Meta.model.objects.create(**data)
    #     print(connection.queries)
    #     instance.created_by = self.context.get('request').user

    #     if users :
    #         for user in users :
    #             instance.user.add(user)
    #     print(connection.queries)
    #     instance.save()
    #     return instance

    def validate_user(self, users):
        lst_invalid = []
        for user in users:
            if not user.is_active:
                lst_invalid.append("{} is not active".format(user.id))
        if lst_invalid:
            raise serializers.ValidationError(lst_invalid)
        return users


class GetRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'
        

class BulkDeteleRoleSerializer(BulkSerializer):
    
    class Meta : 
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
    
    class Meta : 
        model = Permission
        fields = ['ids']