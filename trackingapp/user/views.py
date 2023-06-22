from .serializers import PostUserModelSerializer, GetUserModelSerializer, LoginSerializer
from .models import User
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import authenticate

from django.contrib.auth import login, logout
from baseapp.views import CustomModelViewSetBase


class UserModelViewSet(CustomModelViewSetBase):
    serializer_class = {"create": PostUserModelSerializer, "update": PostUserModelSerializer,
                        "parital_update": PostUserModelSerializer, "default": GetUserModelSerializer}
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class AuthenicationViewSet(CustomModelViewSetBase):
    serializer_class = {"login": LoginSerializer, "default" : LoginSerializer}
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
        if user:
            login(request, user)
            return Response("success")
        return Response("fail")

    @action(methods=['post'], detail=False, url_path="logout")
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
