from django_filters import rest_framework as filter
from media.models import Media
from django.db.models import JSONField


class MediaFilter(filter.FilterSet):
    
    class Meta:
        model = Media
        fields = ['media_from', 'media_to', 'content_type', 'sending_method', 'status', 'created_by']
        filter_overrides = {
            JSONField : {
                "filter_class" : filter.CharFilter,
                "extra" : lambda f : {
                    'lookup_expr' : 'exact'
                }
            }
        }
    