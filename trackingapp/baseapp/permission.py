from rest_framework.permissions import BasePermission
from permissions.models import Role, Permission
from user.models import User
from django.db import connection, reset_queries
from functools import reduce
import functools
import time

def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print("Function : " + func.__name__)
        print("Number of Queries : {}".format(end_queries - start_queries))
        print("Finished in : {}".format(end - start))

        return result

    return inner_func

class CustomPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        permission_lst = request.user.permission_code_names
        
        for perm in permission_lst:
            if perm == 'all':
                return True
            if view.basename == 'user':
                role, action = perm.split('.')
                if role == "admin" :
                    if view.action == action:
                        return True
                else :
                    if view.detail:
                        if str(request.user.id) == (view.kwargs.get('pk') or ' '):
                            return True
        return False
