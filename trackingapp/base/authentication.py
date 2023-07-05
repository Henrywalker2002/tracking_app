from rest_framework.authentication import SessionAuthentication
from functools import reduce
from base.decorators import log_debugger

class CustomAuthentication(SessionAuthentication):
    """
    Add permisson_code_names to request.user
    """
    def authenticate(self, request):

        user = getattr(request._request, 'user', None)
        if not user or not user.is_active:
            return None
        self.enforce_csrf(request)
        perm_lst = reduce(lambda prev, curr: prev + list(
            curr.permission.all().values_list('code_name', flat=True)), user.roles.all(), [])
        setattr(user, 'permission_code_names', perm_lst)
        return (user, None)
