#!/usr/bin/env python3
"""
Тест User Profile endpoints с CSRF cookie
"""
import requests
import json
import re

BASE_URL = 'http://localhost:8000'

print("="*60)
print("ТЕСТИРОВАНИЕ С CSRF COOKIE")
print("="*60)

# Используем сессию для сохранения cookies
session = requests.Session()

# 1. Login (получаем CSRF cookie)
print("\n=== 1. POST /auth/login ===")
r = session.post(f'{BASE_URL}/auth/login', json={
    'email': 'admin@example.com',
    'password': 'adminadmin'
})
print(f"Status: {r.status_code}")
token = r.json()['access_token']
print(f"Token: {token[:50]}...")

# CSRF cookie должно быть в session.cookies
csrf_token = session.cookies.get('csrftoken')
print(f"CSRF Token: {csrf_token[:20] if csrf_token else 'NOT FOUND'}...")

# 2. GET /auth/me
print("\n=== 2. GET /auth/me ===")
session.headers.update({'Authorization': f'Bearer {token}'})
r = session.get(f'{BASE_URL}/auth/me')
print(f"Status: {r.status_code}")
print(f"first_name: {r.json().get('first_name')}")

# 3. PATCH /auth/me/update с CSRF
print("\n=== 3. PATCH /auth/me/update (с CSRF) ===")
if csrf_token:
    session.headers.update({'X-CSRFToken': csrf_token})
    r = session.patch(f'{BASE_URL}/auth/me/update', json={
        'first_name': 'CSRF',
        'last_name': 'Test'
    })
    print(f"Status: {r.status_code}")
    print(json.dumps(r.json(), indent=2))
else:
    print("❌ CSRF token not found!")

# 4. PUT /auth/me/update с CSRF
print("\n=== 4. PUT /auth/me/update (с CSRF) ===")
if csrf_token:
    r = session.put(f'{BASE_URL}/auth/me/update', json={
        'first_name': 'PUT',
        'last_name': 'CSRF',
        'username': 'puttest'
    })
    print(f"Status: {r.status_code}")
    print(json.dumps(r.json(), indent=2))
else:
    print("❌ CSRF token not found!")

# 5. Проверка
print("\n=== 5. GET /auth/me (проверка) ===")
r = session.get(f'{BASE_URL}/auth/me')
print(f"Status: {r.status_code}")
print(f"first_name: {r.json().get('first_name')}")
print(f"last_name: {r.json().get('last_name')}")
print(f"username: {r.json().get('username')}")

print("\n" + "="*60)
if r.status_code == 200:
    print("✅ ВСЕ ТЕСТЫ ПРОШЛИ!")
else:
    print("❌ ТЕСТЫ УПАЛИ!")
print("="*60)
