from django_filters import rest_framework as filter


class TimeTrackingFilter(filter.FilterSet):
    
    release_id = filter.UUIDFilter(field_name= 'release_id', )
    user_id = filter.UUIDFilter(field_name="user_id")
    created_by = filter.UUIDFilter(field_name= "created_by")
    min_start_time = filter.DateTimeFilter(field_name= 'start_time', lookup_expr= 'gte')
    max_end_time = filter.DateTimeFilter(field_name= 'end_time', lookup_expr= 'lte')
    