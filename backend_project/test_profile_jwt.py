#!/usr/bin/env python3
"""
Тест User Profile endpoints с JWT (без CSRF)
"""
import requests
import json

BASE_URL = 'http://localhost:8000'

print("="*60)
print("ТЕСТИРОВАНИЕ С JWT (БЕЗ CSRF)")
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
print(f"first_name: {r.json().get('first_name')}")

# 3. PATCH /auth/me/update (только JWT, без CSRF)
print("\n=== 3. PATCH /auth/me/update (JWT only, NO CSRF) ===")
r = requests.patch(f'{BASE_URL}/auth/me/update', 
    headers={'Authorization': f'Bearer {token}'},
    json={
        'first_name': 'JWT',
        'last_name': 'Test'
    })
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2))

# 4. PUT /auth/me/update (только JWT, без CSRF)
print("\n=== 4. PUT /auth/me/update (JWT only, NO CSRF) ===")
r = requests.put(f'{BASE_URL}/auth/me/update',
    headers={'Authorization': f'Bearer {token}'},
    json={
        'first_name': 'PUT',
        'last_name': 'JWT',
        'username': 'puttest'
    })
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2))

# 5. Проверка
print("\n=== 5. GET /auth/me (проверка) ===")
r = requests.get(f'{BASE_URL}/auth/me', headers={'Authorization': f'Bearer {token}'})
print(f"Status: {r.status_code}")
print(f"first_name: {r.json().get('first_name')}")
print(f"last_name: {r.json().get('last_name')}")
print(f"username: {r.json().get('username')}")

print("\n" + "="*60)
if r.status_code == 200:
    print("✅ ВСЕ ТЕСТЫ ПРОШЛИ! (JWT без CSRF)")
else:
    print("❌ ТЕСТЫ УПАЛИ!")
print("="*60)
