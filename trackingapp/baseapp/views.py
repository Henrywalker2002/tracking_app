from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import logging

class CustomModelViewSetBase(viewsets.ModelViewSet):
    """
    custom get serializer class to get serializer class base on dict 
    Add action bulk detele
    """
    serializer_class = {}
    def get_serializer_class(self):
        if self.action in self.serializer_class.keys():
            return self.serializer_class[self.action]
        return self.serializer_class['default']
    
    def add_serilizer_class(self, key: str, value):
        """
        key is action name , value is serializer class. Example : add_serializer_class("create", PostSerializer)
        """
        self.serializer_class.update({key, value})
        
    @action(methods= ['delete'], detail= False, url_path= 'bulk-delete')
    def bulk_delete(self, request, *args, **kwargs):
        logging.info('{} begin to bulk_delete function'.format(request.content_params.get('id')))
        queryset = self.get_queryset()
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        queryset.filter(id__in = serializer.data['ids']).delete()
        logging.info('{} end bulk_delete function'.format(request.content_params.get('id')))
        return Response(status= status.HTTP_204_NO_CONTENT)
        

    