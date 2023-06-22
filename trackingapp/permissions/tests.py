from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient
import json 
from django.urls import reverse
from rest_framework import status
from .models import Permission
from user.models import User
import unittest
from django.urls import path
from unittest.mock import patch, Mock

factory = APIRequestFactory()
from permissions.views import PermissionModelViewSet

class TestPermission(APITestCase):

    @classmethod 
    def setUpTestData(self):
        data_user = {
            "email": "user@example.com",
            "password": "string",
            "first_name": "string",
            "last_name": "string",
            "phone": "0845123657"
        }
        user = User.objects.create(**data_user)
        data = {"code_name" : "user.edit" , "friendly_name" : "User Edit", "created_by" : user}
        Permission.objects.create(**data)
        
    def setUp(self):
        self.url = reverse("permission-list")
        user = User.objects.get(email = "user@example.com")
        self.client.force_login(user)
        self.count = Permission.objects.count()
        self.permission_instance = Permission.objects.get(code_name = "user.edit")
    
    def test_post_permission(self):
        """
        Ensure can not add with the same code name 
        """
        data = {"code_name" : "user.edit" , "friendly_name" : "User Edit"}
        response = self.client.post(self.url, data = data, format= 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_add_permission(self):
        data = {"code_name" : "user.create", "friendly_name" : "User Add"}    
        response = self.client.post(self.url, data = data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Permission.objects.count(), self.count + 1)
        self.assertEqual(response.data['code_name'], data['code_name'])
        
    def test_update_permission(self):
        permission_instance = Permission.objects.get(code_name = "user.edit")
        date = permission_instance.modified_at
        data = {"friendly_name" : "User can edit"}
        response = self.client.patch(self.url + str(permission_instance.id) + '/', data = json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['friendly_name'], data['friendly_name'])
        self.assertNotEqual(response.data['modified_at'], date) 
        
    
    def test_get_permission(self):
        response = self.client.get(self.url + str(self.permission_instance.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code_name'], self.permission_instance.code_name)
        
        
    def test_delete_permission(self):
        response = self.client.delete(self.url + str(self.permission_instance.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.count - 1, Permission.objects.count())
        
    def test_list_permission(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count, len(response.data))
      
    def tearDown(self):
        self.client.logout()
        
if "__name__" == "__main__":
    unittest.main()