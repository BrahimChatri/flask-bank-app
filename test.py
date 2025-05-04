import requests


headers ={
    'Content-Type': 'application/json',
    'Authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NjMyMDYxMywianRpIjoiMGNhYTdmYmQtYmI5ZS00ZDg1LTgyZmUtZThkN2IxZjFlMzBlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3R1c2VyIiwibmJmIjoxNzQ2MzIwNjEzLCJjc3JmIjoiYmU4N2UxNjgtZTdmMy00NDU5LTk2M2QtMjA2OTE4ZTgzZjc5IiwiZXhwIjoxNzQ3NjE2NjEzfQ.A0YR2OsHx6P1nDuY5hw_UJP0vT1VKU0aly6dFNAej10'
}

payload={
    "user_id": "b74b72e3-d8f9-44b8-bad2-fc21c26da0be",
    "username": "testuser",
    "password": "admin1234",
    "first_name": "brahim",
    "last_name": "Doe",
    "email": "tanalt030@gmail.com",
    "is_admin": False,
    "remember_me": True,
    "phone_number": "1234567890",
    "address": "Somewhere Fake Street",
    "date_created": "2025-05-04 15:00:00",
    "date_of_birth": "1990-01-01",
    "transactions": [],
    "token": None,
    "new_password": "admin1234",
}


response = requests.get("http://127.0.0.1:5000/banking/", headers=headers, json=payload)
print(response.status_code)
print(response.json())
