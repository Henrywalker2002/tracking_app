from media.models import Media
from media.serializers import WriteMediaSerializer, ListMediaSerializer, RetriveMediaSerializer
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from base.views import BulkActionBaseModelViewSet
from media.custom_permission import MediaPermission
from media.filters import MediaFilter

    
class MediaViewSet(BulkActionBaseModelViewSet):
    
    queryset = Media.objects.all()
    serializer_class = {"default" : ListMediaSerializer, "create" : WriteMediaSerializer, 
                        "update" : WriteMediaSerializer, "retrieve" : RetriveMediaSerializer}
    
    permission_classes = [MediaPermission]
    filterset_class = MediaFilter