"""
Tests for user profile endpoints
"""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from api.services.auth import EmailAuthService


class UserprofileTestCase(TestCase):
    """Test cases for user profile endpoints"""

    @classmethod
    def setUpTestData(cls):
        cls.test_user = EmailAuthService().register(
            email='profile@example.com',
            password='testpass123',
            first_name='Profile'
        )
        cls.login_credentials = {'email': 'profile@example.com', 'password': 'testpass123'}
        cls.update_data = {'first_name': 'Updated', 'last_name': 'User'}

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('email_login')
        self.user_update_url = reverse('user_update')
        self.user_delete_url = reverse('user_delete')
        self.me_url = reverse('get_current_user')

    def test_11_user_update_patch(self):
        print("\n=== Test 11: PATCH /auth/me/update ===")
        login_response = self.client.post(self.login_url, self.login_credentials, format='json')
        token = login_response.data['access_token']
        self.client.cookies['access_token'] = token
        update_response = self.client.patch(self.user_update_url, self.update_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['first_name'], 'Updated')
        print("✓ PATCH update successful")

    def test_12_user_update_put(self):
        print("\n=== Test 12: PUT /auth/me/update ===")
        login_response = self.client.post(self.login_url, self.login_credentials, format='json')
        token = login_response.data['access_token']
        self.client.cookies['access_token'] = token
        update_response = self.client.put(self.user_update_url, self.update_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        print("✓ PUT update successful")

    def test_13_user_update_without_jwt(self):
        print("\n=== Test 13: UPDATE without JWT ===")
        update_response = self.client.patch(self.user_update_url, self.update_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("✓ Update without JWT correctly rejected")

    def test_14_user_delete(self):
        print("\n=== Test 14: DELETE /auth/me/delete ===")
        delete_user_data = {'email': 'delete_me@example.com', 'password': 'deletepass123', 'first_name': 'Delete'}
        self.client.post(reverse('email_signup'), delete_user_data, format='json')
        login_response = self.client.post(self.login_url, delete_user_data, format='json')
        token = login_response.data['access_token']
        self.client.cookies['access_token'] = token
        delete_response = self.client.delete(self.user_delete_url)
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        login_again = self.client.post(self.login_url, delete_user_data, format='json')
        self.assertEqual(login_again.status_code, status.HTTP_401_UNAUTHORIZED)
        print("✓ Account deleted, login rejected")
