from unittest import mock, TestCase
from base.permission import CustomPermission

class TestUserPermission(TestCase):
    
    def setUp(self):
        self.request = mock.MagicMock()
        self.user = mock.MagicMock()
        self.view = mock.MagicMock()
        self.user.is_authenticated = True
        self.user.id = 1
        self.permission = CustomPermission()
        self.func_has_permission = self.permission.has_permission
    
    def test_permisison(self):
        self.view.action = 'update'
        self.user.permission_code_names = ['user.self']
        self.view.detail = True
        self.view.basename = 'user'
        self.request.user = self.user
        self.assertEqual(self.func_has_permission(self.request, self.view), True)
        
    def test_permisison_2(self):
        self.view.action = 'retrieve'
        self.view.basename = 'user'
        self.view.detail = True
        self.user.permission_code_names = ['user.self']
        self.request.user = self.user
        self.assertEqual(self.func_has_permission(self.request, self.view), True)
    
    def test_permisison_3(self):
        self.view.action = 'list'
        self.view.basename = 'user'
        self.view.detail = False
        self.user.permission_code_names = ['user.self']
        self.request.user = self.user
        self.assertEqual(self.func_has_permission(self.request, self.view), False)
        
    def test_permisison_4(self):
        self.view.action = 'delete'
        self.view.basename = 'user'
        self.view.detail = True
        self.user.permission_code_names = ['user.self']
        self.request.user = self.user
        self.assertEqual(self.func_has_permission(self.request, self.view), True)
        user = mock.MagicMock()
        user.id = 1 
        
        self.assertEqual(self.permission.has_object_permission(self.request, self.view, user), True)
    
    def tearDown(self):
        pass 
    
class TestTimeTrackingPermission(TestCase):
    
    def setUp(self):
        self.request = mock.MagicMock()
        self.user = mock.MagicMock()
        self.view = mock.MagicMock()
        self.view.basename = "timetracking"
        self.user.is_authenticated = True
        self.user.id = 1
        
        permission = CustomPermission()
        self.func_has_permission = permission.has_permission
    
    def test_1(self):
        self.view.action = "list"
        self.user.permission_code_names = ['timetracking.all']
        self.request.user = self.user
        self.assertEqual(self.func_has_permission(self.request, self.view), True)
        
    def test_2(self):
        self.view.action = "update"
        self.user.permission_code_names = ['timetracking.all']
        self.request.user = self.user
        self.assertEqual(self.func_has_permission(self.request, self.view), True)
    
    def test_3(self):
        self.request.method = "GET"
        self.user.permission_code_names = ['timetracking.view']
        self.request.user = self.user
        self.assertEqual(self.func_has_permission(self.request, self.view), True)
    
    def tearDown(self):
        pass 