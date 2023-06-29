from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from user.views import AuthenicationViewSet, UserModelViewSet
from permissions.views import RoleModelViewSet, PermissionModelViewSet 
from time_tracking.views import TimeTrackingViewSet

router = DefaultRouter()
router.register(r'user', UserModelViewSet)
router.register(r'role', RoleModelViewSet)
router.register(r'permission', PermissionModelViewSet, basename='permission')
router.register(r'time-tracking', TimeTrackingViewSet)

schema_view = get_schema_view(openapi.Info(
    "docs", default_version= "v1", public=True ))

urlpatterns = [
    path('docs/', schema_view.with_ui()),
    path('', include(router.urls)),
    path('login/', AuthenicationViewSet.as_view({'post': 'login'})),
    path('logout/', AuthenicationViewSet.as_view({'post' : 'logout'}))
]
