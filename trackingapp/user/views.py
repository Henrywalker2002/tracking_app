from user.serializers import (CreateUserModelSerializer, ReadUserSummarySerializer, ReadUserDetailSerializer, 
                          LoginSerializer, UpdateRolesSerializer, DeleteRolesSerializer, 
                          UpdateUserSerializer, ForgotPasswordSerializer, ResetPassword)
from .models import User
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import authenticate
from rest_framework import status
from django.contrib.auth import login, logout
from base.views import CustomModelViewSetBase
from user.custom_permission import UserPermission
import logging
from trackingapp.custom_middleware import get_current_request_id
from functools import reduce
from base.authentication import CustomAuthentication
from permissions.models import Role
from base.decorators import query_debugger
from user.execute import send_reset_password_code, send_new_password
from rest_framework import viewsets
import string
import random
from user.models import ResetCodeUser
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
import uuid


class UserModelViewSet(CustomModelViewSetBase):
    serializer_class = {"create": CreateUserModelSerializer, "update": UpdateUserSerializer, 
                        "list" : ReadUserSummarySerializer, "retrieve" : ReadUserDetailSerializer,
                        "partial_update": UpdateUserSerializer, "update_role": UpdateRolesSerializer,
                        "default": ReadUserDetailSerializer, "delete_role" : DeleteRolesSerializer}
    queryset = User.objects.all()
    permission_classes = [UserPermission]
    authentication_classes = [CustomAuthentication]
    search_fields = ['first_name', 'last_name', 'email']
    filterset_fields = ['email', 'phone', 'is_active']
    
    
    @action(methods=['patch'], detail=True, url_path="update-role")
    def update_role(self, request, *args, **kwargs):
        """
        Append role to user
        """
        return super().update(request, *args, **kwargs)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        user = serializer.instance
        password = str(uuid.uuid4())[:8]
        user.set_password(password)
        user.save()
        send_new_password(password, user.email)
        
        serializer_return = self.get_serializer(user, is_get = True)
        return Response(data = serializer_return.data, status= 201)
    
    def update(self, request, *args, **kwargs):
        """
        Set hash password for db
        """
        partial = kwargs.pop('partial', False)
        password = None 
        if 'password' in request.data.keys():
            password = request.data.get('password')
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if password: 
            instance.set_password(password)
            instance.save()

        serializer_return = self.get_serializer(instance, is_get = True)
        
        return Response(serializer_return.data)

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
        serializer_return = self.get_serializer(instance, is_get= True)
        return Response(serializer_return.data)

class AuthenicationViewSet(viewsets.GenericViewSet):
    serializer_class = {"login": LoginSerializer,"send_code" : ForgotPasswordSerializer , 
                        "reset_password" : ResetPassword, "default": LoginSerializer}
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_class(self):
        if self.action in self.serializer_class.keys():
            return self.serializer_class[self.action]
        return self.serializer_class['default']

    def get_permissions(self):
        if self.action == "logout":
            return [permissions.IsAuthenticated()]
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
                return Response("user is not active", status= status.HTTP_401_UNAUTHORIZED)
            login(request, user)
            permission_code_names = reduce(lambda prev, curr: prev | set(
                    curr.permission.all().values_list('code_name', flat=True)), user.roles.all(), set())
            user_data = self.get_serializer(user).data 
            user_data.setdefault('permission_code_names', permission_code_names)
            return Response(user_data)
        return Response({"messsage" : "wrong username or password"}, status= status.HTTP_401_UNAUTHORIZED)

    @action(methods=['post'], detail=False, url_path="logout")
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods= ['post'], detail= False, url_path='forgot-password')
    def send_code(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        code = str(uuid.uuid4())[:6]
        obj, created = ResetCodeUser.objects.update_or_create(
            email = serializer.data.get('email'), defaults = {"code" : code, "expired_time" : timezone.now() + timedelta(days= 1)})
        send_reset_password_code(code, serializer.data.get('email'))
        return Response({"message" : "success"} ,status= status.HTTP_200_OK)

    @action(methods= ['patch'], detail= False, url_path='reset-password')
    def reset_password(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        instance = ResetCodeUser.objects.filter(email = serializer.data.get('email'), 
                                 code = serializer.data.get('code'), expired_time__gte = timezone.now())
        if instance:
            user = User.objects.get(email = serializer.data.get('email'))
            user.set_password(serializer.data.get('password'))
            user.save()
            instance.delete()
            return Response({"message" : "success"} ,status= status.HTTP_200_OK)
        else :
            return Response(data = {"code" : ["wrong code or code expired"]}, status=status.HTTP_400_BAD_REQUEST)