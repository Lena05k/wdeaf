"""
Tests for provider endpoints
"""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse


class ProviderTestCase(TestCase):
    """Test cases for provider endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.provider_signup_url = reverse('provider_signup')
        self.provider_list_url = reverse('provider_list')
        self.provider_data = {
            'email': 'provider_test@example.com',
            'password': 'providerpass123',
            'first_name': 'Provider',
            'last_name': 'Test',
            'phone': '+77771234567'
        }

    def test_15_provider_signup(self):
        print("\n=== Test 15: Provider Signup ===")
        signup_response = self.client.post(self.provider_signup_url, self.provider_data, format='json')
        self.assertEqual(signup_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', signup_response.data)
        self.assertEqual(signup_response.data['user']['is_provider'], True)
        print("✓ Provider signup successful")

    def test_16_provider_list(self):
        print("\n=== Test 16: Provider List ===")
        self.client.post(self.provider_signup_url, self.provider_data, format='json')
        list_response = self.client.get(self.provider_list_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertIn('count', list_response.data)
        self.assertIn('results', list_response.data)
        print(f"✓ Provider list retrieved (count: {list_response.data['count']})")

    def test_17_provider_duplicate_signup(self):
        print("\n=== Test 17: Duplicate Provider Signup ===")
        self.client.post(self.provider_signup_url, self.provider_data, format='json')
        duplicate_response = self.client.post(self.provider_signup_url, self.provider_data, format='json')
        self.assertEqual(duplicate_response.status_code, status.HTTP_409_CONFLICT)
        print("✓ Duplicate provider signup correctly rejected")
