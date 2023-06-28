from .serializers import WriteUserModelSerializer, GetUserModelSerializer, LoginSerializer, UpdateRolesSerializer
from .models import User, AppUser
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

class UserModelViewSet(CustomModelViewSetBase):
    serializer_class = {"create": WriteUserModelSerializer, "update": WriteUserModelSerializer,
                        "partial_update": WriteUserModelSerializer, "update_role": UpdateRolesSerializer, 
                        "default": GetUserModelSerializer, "bulk_create" : WriteUserModelSerializer}
    queryset = User.objects.all()
    permission_classes = [CustomPermission]
    authentication_classes = [CustomAuthentication]

    @action(methods=['patch', 'put'], detail=True, url_path="update-role")
    def update_role(self, request, *args, **kwargs):
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


class AuthenicationViewSet(CustomModelViewSetBase):
    serializer_class = {"login": LoginSerializer, "default": LoginSerializer}
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == "login":
            return [permissions.AllowAny()]
        return super().get_permissions()

    @action(methods=['post'], detail=False, url_path="login")
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request, username=serializer.validated_data['email'], password=serializer.validated_data['password'])
        # user = authenticate(serializer.validated_data['email'], serializer.validated_data['password'])
        if user:
            if not user.is_active:
                return Response("user is not active")
            login(request, user)
            return Response(self.get_serializer(user).data)
        return Response("wrong username or password")

    @action(methods=['post'], detail=False, url_path="logout")
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
