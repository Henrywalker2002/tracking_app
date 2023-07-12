from user.serializers import (CreateUserModelSerializer, GetUserModelSerializer,
                          LoginSerializer, UpdateRolesSerializer, DeleteRolesSerializer, 
                          BulkUpdateUserSerializer, UpdateUserSerializer, ForgotPasswordSerializer)
from .models import User
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import authenticate
from rest_framework import status
from django.contrib.auth import login, logout
from base.views import CustomModelViewSetBase
from base.permission import CustomPermission
import logging
from trackingapp.custom_middleware import get_current_request_id
from functools import reduce
from base.authentication import CustomAuthentication
from permissions.models import Role
from base.decorators import query_debugger
from media.execute import send_new_password
import string
import random

class UserModelViewSet(CustomModelViewSetBase):
    serializer_class = {"create": CreateUserModelSerializer, "update": UpdateUserSerializer,
                        "partial_update": UpdateUserSerializer, "update_role": UpdateRolesSerializer,
                        "default": GetUserModelSerializer, "bulk_create": CreateUserModelSerializer,
                        "bulk_update": BulkUpdateUserSerializer, "delete_role" : DeleteRolesSerializer}
    queryset = User.objects.all()
    permission_classes = [CustomPermission]
    authentication_classes = [CustomAuthentication]
    
    @action(methods=['patch'], detail=True, url_path="update-role")
    def update_role(self, request, *args, **kwargs):
        """
        Append role to user
        """
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        id = get_current_request_id()
        logging.info(f'request id {id} begin to list user')
        instance_list = super().list(request, *args, **kwargs)
        logging.info(f'request id {id} end to list user')
        return instance_list

    @action(detail=True, url_path="get-role")
    def get_role(self, request, pk):
        instance = User.objects.prefetch_related('roles')
        roles_name = reduce(lambda prev, curr: prev + list(curr.roles.all().values_list(
            'friendly_name', flat=True)), instance.filter(id=pk), [])
        return Response(roles_name)

    @action(detail= True, url_path="delete-role", methods= ['patch'])
    def delete_role(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        [instance.roles.remove(Role.objects.get(id = id)) for id in request.data.get('roles')]
        return Response()

class AuthenicationViewSet(CustomModelViewSetBase):
    serializer_class = {"login": LoginSerializer,"reset_password" : ForgotPasswordSerializer , "default": LoginSerializer}
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == "login":
            return [permissions.AllowAny()]
        return super().get_permissions()

    @action(methods=['post'], detail=False, url_path="login")
    @query_debugger
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            request, username=serializer.validated_data['email'], password=serializer.validated_data['password'])
        if user:
            if not user.is_active:
                return Response("user is not active")
            login(request, user)
            permission_code_names = reduce(lambda prev, curr: prev + list(
                    curr.permission.all().values_list('code_name', flat=True)), user.roles.all(), [])
            user_data = self.get_serializer(user).data 
            user_data.setdefault('permission_code_names', permission_code_names)
            return Response(user_data)
        return Response("wrong username or password")

    @action(methods=['post'], detail=False, url_path="logout")
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods= ['patch'], detail= False, url_path='forgot-password')
    def reset_password(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid()
        instance = User.objects.get(email = serializer.data.get("email"))
        password = ''.join(random.choices(string.ascii_uppercase 
                                          + string.ascii_lowercase + string.digits, k = 8))
        instance.set_password(password)
        send_new_password(password, serializer.data.get("email"))
        instance.save()
        return Response(status= status.HTTP_204_NO_CONTENT)
