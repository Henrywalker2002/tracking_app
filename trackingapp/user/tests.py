from rest_framework.test import APITestCase
from unittest.mock import patch
from user.models import User
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from dateutil import parser
import datetime

class TestUser(APITestCase):
    now = timezone.now()
    @classmethod 
    def setUpTestData(self):
        data_user = {
            "email": "user@example.com",
            "password": "string123",
            "first_name": "string",
            "last_name": "string",
            "phone": "0845123657"
        }
        user = User.objects.create(**data_user)
    
    def setUp(self):
        self.url = reverse('user-list')
        user = User.objects.get(email = "user@example.com")
        self.client.force_login(user)
        
    def test_create_user_1(self):
        response = self.client.post(self.url, data = {}, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @patch('user.views.UserModelViewSet.check_permissions', return_value = True)
    def test_create_user_2(self, mock):
        data = {
            "email": "user@example.com",
            "password": "string123",
            "first_name": "string",
            "last_name": "string",
            "phone": "phone"
        }
        response = self.client.post(self.url, data = data, format = 'json')
        NUMBER_ERROR = 2
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.json()), NUMBER_ERROR)
    
    @patch('user.views.UserModelViewSet.check_permissions', return_value = True)
    @patch('django.utils.timezone.now', return_value = now)
    def test_create_user_3(self, mock1, mock2):
        data = {
            "email": "user123@example.com",
            "password": "string123",
            "first_name": "string",
            "last_name": "string",
            "phone": "0652369541"
        }
        response = self.client.post(self.url, data = data, format = 'json')
        json = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_at = parser.parse(json.get('created_at'))
        self.assertEqual(created_at, self.now)
        self.assertEqual(len(json), 8)
    
    @patch('user.views.UserModelViewSet.check_permissions', return_value = True)
    def test_update_user(self, mock):
        user = User.objects.get(email = "user@example.com")
        data = {
            "first_name": "name"
        }
        response = self.client.patch(f'{self.url}{user.id}/', data = data, format = 'json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('first_name'), 'name')
    
    @patch('user.views.UserModelViewSet.check_permissions', return_value = True)
    def test_delete_user(self, mock):
        response = self.client.delete(f'{self.url}{123}/', data = {}, format = 'json')
        self.assertEqual(response.status_code, 404)
        
    @patch('user.views.UserModelViewSet.check_permissions', return_value = True)
    def test_delete_user_2(self, mock):
        count = len(User.objects.all())
        user = User.objects.get(email = "user@example.com")
        response = self.client.delete(f'{self.url}{user.id}/', data = {}, format = 'json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(User.objects.all()), count - 1)
    
    def tearDown(self):
        self.client.logout()