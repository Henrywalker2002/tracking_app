from unittest import mock, TestCase
from base.permission import CustomPermission

class TestPermission(TestCase):
    
    def setUp(self):
        self.request = mock.MagicMock()
        self.user = mock.MagicMock()
        self.view = mock.MagicMock()
        self.user.is_authenticated = True
        self.permission = CustomPermission()
        self.func_has_permission = self.permission.has_permission
    
    def test_permisison(self):
        self.view.action = 'update'
        self.user.permission_code_names = ['user.edit']
        self.view.basename = 'user'
        self.request.user = self.user
        self.assertEqual(self.func_has_permission(self.request, self.view), False)
        
    def test_permisison_2(self):
        self.view.action = 'retrieve'
        self.view.basename = 'user'
        self.user.permission_code_names = ['admin.retrieve']
        self.request.user = self.user
        self.assertEqual(self.func_has_permission(self.request, self.view), True)
    
    def tearDown(self):
        pass 