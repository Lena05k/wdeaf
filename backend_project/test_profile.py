#!/usr/bin/env python3
import requests
import json

BASE_URL = 'http://localhost:8000'

# 1. Login
print("=== 1. Login ===")
r = requests.post(f'{BASE_URL}/auth/login', json={
    'email': 'admin@example.com',
    'password': 'adminadmin'
})
token = r.json()['access_token']
print(f"Token: {token[:50]}...")

# 2. Get current user
print("\n=== 2. GET /auth/me ===")
r = requests.get(f'{BASE_URL}/auth/me', headers={'Authorization': f'Bearer {token}'})
print(json.dumps(r.json(), indent=2))

# 3. Update profile (PATCH)
print("\n=== 3. PATCH /auth/me/update ===")
r = requests.patch(f'{BASE_URL}/auth/me/update', 
    headers={'Authorization': f'Bearer {token}'},
    json={'first_name': 'Updated', 'last_name': 'Admin'})
print(json.dumps(r.json(), indent=2))

# 4. Update profile (PUT - full update)
print("\n=== 4. PUT /auth/me/update ===")
r = requests.put(f'{BASE_URL}/auth/me/update',
    headers={'Authorization': f'Bearer {token}'},
    json={'first_name': 'Full', 'last_name': 'Update', 'username': 'fullupdate'})
print(json.dumps(r.json(), indent=2))

print("\n✅ Все тесты прошли!")
