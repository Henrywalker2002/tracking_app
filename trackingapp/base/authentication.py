from rest_framework.authentication import SessionAuthentication
from functools import reduce


class CustomAuthentication(SessionAuthentication):
    def authenticate(self, request):

        user = getattr(request._request, 'user', None)
        if not user or not user.is_active:
            return None
        self.enforce_csrf(request)
        perm_lst = reduce(lambda prev, curr: prev + list(
            curr.permission.all().values_list('code_name', flat=True)), user.roles.all(), [])
        setattr(user, 'perm_lst', perm_lst)
        return (user, None)
