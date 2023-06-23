from rest_framework.permissions import BasePermission
from permissions.models import Role, Permission
from user.models import User
from django.db import connection, reset_queries

def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

class CustomPermission(BasePermission):

    def has_permission(self, request, view):
        cursor = connection.cursor()
        cursor.execute("""
            select * 
            from permissions_permission 
            where permissions_permission.id in (
                select permission_id 
                from permissions_role_permission 
                where role_id in (
                    select role_id 
                    from user_user_roles 
                    where user_id = %s
                )
            ) 
        """, [request.user.id])

        permission_lst = dictfetchall(cursor)
        for perm in permission_lst:
            if perm['code_name'] == 'all':
                return True
            if view.basename == 'user':
                role, action = perm['code_name'].split('.')
                if role == "admin" :
                    if view.action == action:
                        return True
                else :
                    if view.detail:
                        if str(request.user.id) == (view.kwargs.get('pk') or ' '):
                            return True
        return False
