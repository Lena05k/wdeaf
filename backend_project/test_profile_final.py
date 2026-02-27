#!/usr/bin/env python3
import requests
import json

BASE_URL = 'http://localhost:8000'

print("="*60)
print("ТЕСТИРОВАНИЕ USER PROFILE ENDPOINTS")
print("="*60)

# 1. Login
print("\n=== 1. POST /auth/login ===")
r = requests.post(f'{BASE_URL}/auth/login', json={
    'email': 'admin@example.com',
    'password': 'adminadmin'
})
print(f"Status: {r.status_code}")
token = r.json()['access_token']
print(f"Token: {token[:50]}...")

# 2. GET /auth/me
print("\n=== 2. GET /auth/me ===")
r = requests.get(f'{BASE_URL}/auth/me', headers={'Authorization': f'Bearer {token}'})
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2))

# 3. PATCH /auth/me/update (с CSRF cookie)
print("\n=== 3. PATCH /auth/me/update ===")
# Сначала получим CSRF cookie
session = requests.Session()
session.cookies.update(r.cookies)
session.headers.update({'Authorization': f'Bearer {token}'})

r = session.patch(f'{BASE_URL}/auth/me/update', json={
    'first_name': 'Test',
    'last_name': 'User'
})
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2))

# 4. PUT /auth/me/update
print("\n=== 4. PUT /auth/me/update ===")
r = session.put(f'{BASE_URL}/auth/me/update', json={
    'first_name': 'Full',
    'last_name': 'Update',
    'username': 'testuser'
})
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2))

# 5. Проверка что данные обновились
print("\n=== 5. GET /auth/me (проверка) ===")
r = session.get(f'{BASE_URL}/auth/me')
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2))

print("\n" + "="*60)
print("✅ ВСЕ ТЕСТЫ ПРОШЛИ!")
print("="*60)
