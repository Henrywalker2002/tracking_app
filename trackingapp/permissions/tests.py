from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient
import json
from django.urls import reverse
from rest_framework import status
from permissions.models import Permission, Role
from user.models import User
from unittest.mock import patch
from django.urls import path

factory = APIRequestFactory()


class TestPermission(APITestCase):

    @classmethod
    def setUpTestData(self):
        data_user = {
            "email": "user@example.com",
            "password": "string12345",
            "first_name": "string",
            "last_name": "string",
            "phone": "0845123657"
        }
        self.user = User.objects.create(**data_user)
        
        @patch('base.models.get_current_user', return_value = self.user)
        def create_data(mock):
            data = {"code_name": "user.edit",
                    "friendly_name": "User Edit"}
            Permission.objects.create(**data)
        
        create_data()
        
    def setUp(self):
        self.url = reverse("permission-list")
        self.user = User.objects.get(email="user@example.com")
        self.client.force_login(self.user)
        self.count = Permission.objects.count()
        self.permission_instance = Permission.objects.get(code_name = "user.edit")

    @patch("permissions.views.PermissionModelViewSet.check_permissions", return_value=None)
    def test_post_permission(self, mocker):
        data = {"code_name": "user.edit", "friendly_name": "User Edit"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, 400)

    @patch("permissions.views.PermissionModelViewSet.check_permissions", return_value=None)
    def test_add_permission(self, mock):
        data = {"code_name": "user.create", "friendly_name": "User Add"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Permission.objects.count(), self.count + 1)
        self.assertEqual(response.data['code_name'], data['code_name'])

    @patch("permissions.views.PermissionModelViewSet.check_permissions", return_value=None)
    def test_update_permission(self, mock):
        permission_instance = Permission.objects.get(code_name="user.edit")
        date = permission_instance.modified_at
        data = {"friendly_name": "User can edit"}
        response = self.client.patch(self.url + str(permission_instance.id) +
                                     '/', data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['friendly_name'], data['friendly_name'])
        self.assertNotEqual(response.data['modified_at'], date)

    @patch("permissions.views.PermissionModelViewSet.check_permissions", return_value=None)
    def test_get_permission(self, mock):
        response = self.client.get(
            self.url + str(self.permission_instance.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code_name'],
                         self.permission_instance.code_name)

    @patch("permissions.views.PermissionModelViewSet.check_permissions", return_value=None)
    def test_delete_permission(self, mock):
        response = self.client.delete(
            self.url + str(self.permission_instance.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.count - 1, Permission.objects.count())

    @patch("permissions.views.PermissionModelViewSet.check_permissions", return_value=None)
    def test_list_permission(self, mock):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @patch("permissions.views.PermissionModelViewSet.check_permissions", return_value=None)
    def test_bulk_create(self, mock):
        data = [
            {
                "friendly_name" : "test123",
                "code_name" : "test123",
            },
            {
                "friendly_name" : "test13",
                "code_name" : "test13",
            }
        ]
        response = self.client.post(f'{self.url}bulk-create/', data= data, format = 'json')
        json = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(json), 2)
        
    def test_permission(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        self.client.logout()

class TestRole(APITestCase):
    
    @classmethod
    def setUpTestData(self):
        data_user = {
            "email": "user@example.com",
            "password": "string12345",
            "first_name": "string",
            "last_name": "string",
            "phone": "0845123657"
        }
        self.user = User.objects.create(**data_user)
        
        @patch('base.models.get_current_user', return_value = self.user)
        def create_data(mock):
            
            perm_data = {"code_name": "user.edit",
                    "friendly_name": "User Edit"}
            permission = Permission.objects.create(**perm_data)
            role_data = {"code_name": "user",
                    "friendly_name": "User"}
            role = Role.objects.create(**role_data)
            role.permission.set([permission])
        create_data()
    
    def setUp(self):
        self.url = reverse('role-list')
        self.user = User.objects.get(email = "user@example.com")
        self.client.force_login(self.user) 
        self.count = len(Role.objects.all())
        self.role_instance = Role.objects.get(code_name = "user")
        self.permission_instance = Permission.objects.get(code_name= 'user.edit')
    
    def test_post(self):
        # test permisison
        data = {
            "code_name" : "user",
            "friendly_name" : "test"
        }
        response = self.client.post(self.url, data = data, format = "json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    @patch('permissions.views.RoleModelViewSet.check_permissions', return_value = None)
    def test_post_2(self, mock):
        # test equal code name
        data = {
            "code_name" : "user",
            "friendly_name" : "test"
        }
        response = self.client.post(self.url, data = data, format = "json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    @patch('permissions.views.RoleModelViewSet.check_permissions', return_value = None)
    def test_post_3(self, mock):

        data = {
            "code_name" : "admin",
            "friendly_name" : "test", 
            "permission" : [
                str(self.permission_instance.id)
            ]
        }
        response = self.client.post(self.url, data = data, format = "json")
        json = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    @patch('permissions.views.RoleModelViewSet.check_permissions', return_value = None)
    def test_update(self, mock):

        data = {
            "code_name" : "Admin",
            "friendly_name" : "test", 
        }
        response = self.client.patch(f'{self.url}{self.role_instance.id}/', data = data, format = "json")
        json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.get('code_name'), data.get('code_name'))
        
    @patch('permissions.views.RoleModelViewSet.check_permissions', return_value = None)
    def test_update(self, mock):
        
        response = self.client.delete(f'{self.url}{self.role_instance.id}/', format = "json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.count - 1, len(Role.objects.all()))
    
    def tearDown(self):
        self.client.logout()
