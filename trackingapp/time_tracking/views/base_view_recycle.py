from base.views import BulkActionBaseModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models.query import QuerySet


class BaseViewRecycle(BulkActionBaseModelViewSet):
    """
    Base for model which have is_deleted fields.
    Custom queryset, restore, auto deleted in background action
    """

    def get_queryset(self):
        """
        Override to get only instance which is_deleted is False or deleted instance 
        """
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            if self.action not in ["get_time_tracking_deleted", "restore"]:
                queryset = queryset.filter(is_deleted=False)
            else:
                queryset = queryset.filter(is_deleted=True)
        return queryset

    def destroy(self, request, *args, **kwargs):
        """
        Only set is_deleted = False for being deleted later by auto delete job
        """
        instance = self.get_object()
        if not instance.is_deleted:
            setattr(instance, 'is_deleted', True)
            instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, url_path='recycle')
    def get_time_tracking_deleted(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, url_path='recycle', methods=['put'])
    def restore(self, request, pk):
        instance = self.get_object()
        instance.is_deleted = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
