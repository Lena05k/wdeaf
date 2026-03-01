"""
Tests for authentication endpoints
"""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from api.services.auth import EmailAuthService


class AuthTestCase(TestCase):
    """Test cases for authentication endpoints"""

    @classmethod
    def setUpTestData(cls):
        """Create test user once for all tests"""
        cls.test_user = EmailAuthService().register(
            email='test@example.com',
            password='testpass123',
            first_name='Test'
        )
        cls.new_user_data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'first_name': 'NewUser'
        }

    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('email_signup')
        self.login_url = reverse('email_login')
        self.logout_url = reverse('logout')
        self.me_url = reverse('get_current_user')
        self.user_update_url = reverse('user_update')
        self.user_delete_url = reverse('user_delete')
        self.login_credentials = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        self.update_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'username': 'updateduser'
        }

    def test_01_signup(self):
        print("\n=== Test 1: Signup ===")
        response = self.client.post(self.signup_url, self.new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        print("✓ Signup successful")

    def test_02_login(self):
        print("\n=== Test 2: Login ===")
        response = self.client.post(self.login_url, self.login_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        print("✓ Login successful")

    def test_03_login_invalid_credentials(self):
        print("\n=== Test 3: Login with invalid credentials ===")
        response = self.client.post(self.login_url, {'email': 'bad@example.com', 'password': 'wrong'}, format='json')
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED])
        print("✓ Invalid login correctly rejected")

    def test_04_logout(self):
        print("\n=== Test 4: Logout ===")
        login_response = self.client.post(self.login_url, self.login_credentials, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        logout_response = self.client.post(self.logout_url)
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        print("✓ Logout successful")

    def test_05_logout_already_logged_out(self):
        print("\n=== Test 5: Logout when already logged out ===")
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("✓ Logout without token correctly rejected")

    def test_06_me_authenticated(self):
        print("\n=== Test 6: Get current user (authenticated) ===")
        login_response = self.client.post(self.login_url, self.login_credentials, format='json')
        token = login_response.data['access_token']
        self.client.cookies['access_token'] = token
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✓ Get current user successful")

    def test_07_me_unauthenticated(self):
        print("\n=== Test 7: Get current user (unauthenticated) ===")
        response = self.client.get(self.me_url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        print("✓ Unauthenticated access correctly rejected")

    def test_08_logout_twice(self):
        print("\n=== Test 8: Logout twice ===")
        login_response = self.client.post(self.login_url, self.login_credentials, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        first_logout = self.client.post(self.logout_url)
        self.assertEqual(first_logout.status_code, status.HTTP_200_OK)
        self.client.cookies.clear()
        second_logout = self.client.post(self.logout_url)
        self.assertEqual(second_logout.status_code, status.HTTP_401_UNAUTHORIZED)
        print("✓ Second logout correctly rejected")

    def test_09_only_access_token_cookie(self):
        print("\n=== Test 9: Only access_token cookie ===")
        response = self.client.post(self.login_url, self.login_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cookie_names = [key for key in response.cookies.keys()]
        self.assertIn('access_token', cookie_names)
        self.assertNotIn('sessionid', cookie_names)
        self.assertNotIn('csrftoken', cookie_names)
        print("✓ Only access_token cookie set")

    def test_10_full_auth_flow(self):
        print("\n=== Test 10: Full authentication flow ===")
        signup_response = self.client.post(self.signup_url, self.new_user_data, format='json')
        self.assertEqual(signup_response.status_code, status.HTTP_201_CREATED)
        token = signup_response.data['access_token']
        self.client.cookies['access_token'] = token
        me_response = self.client.get(self.me_url)
        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        self.client.cookies.clear()
        logout_response = self.client.post(self.logout_url)
        self.assertEqual(logout_response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("✓ Full flow completed")
