from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from user.views import AuthenicationViewSet, UserModelViewSet
from permissions.views import RoleModelViewSet, PermissionModelViewSet 
from time_tracking.views.history import HistoryViewOnly
from time_tracking.views.subcriber import SubcriberModelViewSet
from time_tracking.views.time_tracking import TimeTrackingViewSet
from time_tracking.views.release import ReleaseModelViewSet
from notification.views import NotificationViewset
from media.views import MediaViewSet
from rest_framework import permissions

router = DefaultRouter()
router.register(r'user', UserModelViewSet)
router.register(r'role', RoleModelViewSet)
router.register(r'permission', PermissionModelViewSet, basename='permission')
router.register(r'time-tracking', TimeTrackingViewSet)
router.register(r'time-tracking-history', HistoryViewOnly, basename="history")
router.register(r'subcriber', SubcriberModelViewSet)
router.register(r'notification', NotificationViewset)
router.register(r'media', MediaViewSet)
router.register(r'release', ReleaseModelViewSet)

schema_view = get_schema_view(openapi.Info(
    "docs", default_version= "v1", public=True ), permission_classes= (permissions.AllowAny ,))

urlpatterns = [
    path('docs/', schema_view.with_ui()),
    path('', include(router.urls)),
    path('login/', AuthenicationViewSet.as_view({'post': 'login'})),
    path('logout/', AuthenicationViewSet.as_view({'post' : 'logout'})),
    path('forgot-password/', AuthenicationViewSet.as_view({'patch' : 'reset_password'}))
]
