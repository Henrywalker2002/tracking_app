from django_filters import rest_framework as filter
from time_tracking.models.release import ReleaseStatus

class ReleaseFilter(filter.FilterSet):
    
    status = filter.MultipleChoiceFilter(field_name= 'status', choices = ReleaseStatus.choices)
    min_start_time = filter.DateTimeFilter(field_name= 'start_time', lookup_expr= 'gte')
    max_end_time = filter.DateTimeFilter(field_name= 'end_time', lookup_expr= 'lte')
    