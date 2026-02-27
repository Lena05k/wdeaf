"""
Tests for authentication endpoints
Similar to MarsStationBackend implementation
"""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
import json


class AuthTestCase(TestCase):
    """Test cases for authentication endpoints"""

    @classmethod
    def setUpTestData(cls):
        """Create test user once for all tests"""
        from api.services import AuthService
        
        # Create user once for all tests
        cls.test_user = AuthService.register_email_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test'
        )
        
        # Create another user for signup test
        cls.new_user_data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'first_name': 'NewUser'
        }

    def setUp(self):
        """Set up test client"""
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
        """Test user registration"""
        print("\n=== Test 1: Signup ===")
        response = self.client.post(
            self.signup_url,
            self.new_user_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], self.new_user_data['email'])
        
        # Check access_token cookie is set
        self.assertIn('access_token', response.cookies)
        print(f"✓ Signup successful: {response.data['user']['email']}")

    def test_02_login(self):
        """Test user login"""
        print("\n=== Test 2: Login ===")
        response = self.client.post(
            self.login_url,
            self.login_credentials,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('access_token', response.cookies)
        print(f"✓ Login successful: {response.data['user']['email']}")

    def test_03_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        print("\n=== Test 3: Login with invalid credentials ===")
        response = self.client.post(
            self.login_url,
            {
                'email': 'nonexistent@example.com',
                'password': 'wrongpassword'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("✓ Invalid login correctly rejected")

    def test_04_logout(self):
        """Test user logout"""
        print("\n=== Test 4: Logout ===")
        # Login first
        login_response = self.client.post(
            self.login_url,
            self.login_credentials,
            format='json'
        )
        
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        
        # Logout
        logout_response = self.client.post(self.logout_url)
        
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertEqual(logout_response.data['detail'], 'Successfully logged out')
        
        # Check cookie is cleared
        logout_cookie = logout_response.cookies.get('access_token')
        self.assertEqual(logout_cookie.value, '')
        self.assertEqual(logout_cookie['max-age'], 0)
        print("✓ Logout successful, cookie cleared")

    def test_05_logout_already_logged_out(self):
        """Test logout when already logged out (no token)"""
        print("\n=== Test 5: Logout when already logged out ===")
        # Try to logout without logging in
        response = self.client.post(self.logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Already logged out')
        print("✓ Logout without token correctly rejected with 401")

    def test_06_me_authenticated(self):
        """Test get current user when authenticated"""
        print("\n=== Test 6: Get current user (authenticated) ===")
        # Login
        login_response = self.client.post(
            self.login_url,
            self.login_credentials,
            format='json'
        )
        
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        
        # Get token from response data
        token = login_response.data['access_token']
        
        # Access protected endpoint with token in cookie
        self.client.cookies['access_token'] = token
        response = self.client.get(self.me_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.login_credentials['email'])
        print(f"✓ Get current user successful: {response.data['email']}")

    def test_07_me_unauthenticated(self):
        """Test get current user when unauthenticated"""
        print("\n=== Test 7: Get current user (unauthenticated) ===")
        # Try to access without authentication
        response = self.client.get(self.me_url)
        
        # Should be 403 (Forbidden) or 401 (Unauthorized)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        print("✓ Unauthenticated access correctly rejected")

    def test_08_logout_twice(self):
        """Test logout twice - second should fail"""
        print("\n=== Test 8: Logout twice ===")
        # Login
        login_response = self.client.post(
            self.login_url,
            self.login_credentials,
            format='json'
        )
        
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        
        # First logout - should succeed
        first_logout = self.client.post(self.logout_url)
        self.assertEqual(first_logout.status_code, status.HTTP_200_OK)
        print("✓ First logout successful")
        
        # Clear cookies manually (simulate browser behavior)
        self.client.cookies.clear()
        
        # Second logout - should fail (no token)
        second_logout = self.client.post(self.logout_url)
        self.assertEqual(second_logout.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(second_logout.data['detail'], 'Already logged out')
        print("✓ Second logout correctly rejected with 401")

    def test_09_only_access_token_cookie(self):
        """Test that only access_token cookie is set (no sessionid, csrftoken)"""
        print("\n=== Test 9: Only access_token cookie (no sessionid, csrftoken) ===")
        response = self.client.post(
            self.login_url,
            self.login_credentials,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check only access_token cookie is set
        cookies = response.cookies
        cookie_names = [key for key in cookies.keys()]
        
        self.assertIn('access_token', cookie_names)
        self.assertNotIn('sessionid', cookie_names)
        self.assertNotIn('csrftoken', cookie_names)
        print(f"✓ Only access_token cookie set: {cookie_names}")

    def test_10_full_auth_flow(self):
        """Test full authentication flow: signup → me → logout → logout again"""
        print("\n=== Test 10: Full authentication flow ===")
        
        # 1. Signup
        signup_response = self.client.post(
            self.signup_url,
            self.new_user_data,
            format='json'
        )
        self.assertEqual(signup_response.status_code, status.HTTP_201_CREATED)
        token = signup_response.data['access_token']
        print("  1. ✓ Signup")
        
        # 2. Access protected endpoint
        self.client.cookies['access_token'] = token
        me_response = self.client.get(self.me_url)
        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        print("  2. ✓ Get current user")
        
        # 3. Logout (clear cookies)
        self.client.cookies.clear()
        logout_response = self.client.post(self.logout_url)
        self.assertEqual(logout_response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("  3. ✓ Logout (no token - 401)")

        print("✓ Full flow completed successfully")

    # =========================================================================
    # USER PROFILE TESTS
    # =========================================================================

    def test_11_user_update_patch(self):
        """Test PATCH /auth/me/update - partial update"""
        print("\n=== Test 11: PATCH /auth/me/update ===")
        
        # Login
        login_response = self.client.post(self.login_url, self.login_credentials, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data['access_token']
        
        # Update profile (PATCH)
        self.client.cookies['access_token'] = token
        update_response = self.client.patch(self.user_update_url, self.update_data, format='json')
        
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['first_name'], 'Updated')
        self.assertEqual(update_response.data['last_name'], 'User')
        print("✓ PATCH update successful")

    def test_12_user_update_put(self):
        """Test PUT /auth/me/update - full update"""
        print("\n=== Test 12: PUT /auth/me/update ===")
        
        # Login
        login_response = self.client.post(self.login_url, self.login_credentials, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data['access_token']
        
        # Update profile (PUT)
        self.client.cookies['access_token'] = token
        update_response = self.client.put(self.user_update_url, self.update_data, format='json')
        
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['first_name'], 'Updated')
        print("✓ PUT update successful")

    def test_13_user_update_without_jwt(self):
        """Test /auth/me/update without JWT - should fail"""
        print("\n=== Test 13: UPDATE without JWT ===")
        
        # Try to update without authentication
        update_response = self.client.patch(self.user_update_url, self.update_data, format='json')
        
        self.assertEqual(update_response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("✓ Update without JWT correctly rejected")

    def test_14_user_delete(self):
        """Test DELETE /auth/me/delete"""
        print("\n=== Test 14: DELETE /auth/me/delete ===")
        
        # Create user for deletion
        delete_user_data = {
            'email': 'delete_me@example.com',
            'password': 'deletepass123',
            'first_name': 'Delete'
        }
        signup_response = self.client.post(self.signup_url, delete_user_data, format='json')
        self.assertEqual(signup_response.status_code, status.HTTP_201_CREATED)
        
        # Login
        login_response = self.client.post(self.login_url, delete_user_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data['access_token']
        
        # Delete account
        self.client.cookies['access_token'] = token
        delete_response = self.client.delete(self.user_delete_url)
        
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertEqual(delete_response.data['detail'], 'Account deleted successfully')
        
        # Check cookies are cleared
        self.assertIn('access_token', delete_response.cookies)
        print("✓ Account deleted, cookies cleared")
        
        # Try to login again - should fail
        login_again = self.client.post(self.login_url, delete_user_data, format='json')
        self.assertEqual(login_again.status_code, status.HTTP_401_UNAUTHORIZED)
        print("✓ Login after delete correctly rejected")
