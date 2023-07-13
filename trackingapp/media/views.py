from media.models import Media
from media.serializers import MediaSerializer
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from base.views import BulkActionBaseModelViewSet

    
class MediaViewSet(BulkActionBaseModelViewSet):
    
    queryset = Media.objects.all()
    serializer_class = {"default" : MediaSerializer}
    
    
    