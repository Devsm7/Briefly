"""Seed 15 users to the database."""
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.app.db.session import SessionLocal
from backend.app.services.auth_service import auth_service
from backend.app.schemas.user import UserCreate

users_data = [
    {"username": "john_doe", "first_name": "John", "last_name": "Doe", "gender": "Male"},
    {"username": "jane_smith", "first_name": "Jane", "last_name": "Smith", "gender": "Female"},
    {"username": "alex_johnson", "first_name": "Alex", "last_name": "Johnson", "gender": "Male"},
    {"username": "emily_brown", "first_name": "Emily", "last_name": "Brown", "gender": "Female"},
    {"username": "michael_wilson", "first_name": "Michael", "last_name": "Wilson", "gender": "Male"},
    {"username": "sarah_davis", "first_name": "Sarah", "last_name": "Davis", "gender": "Female"},
    {"username": "david_miller", "first_name": "David", "last_name": "Miller", "gender": "Male"},
    {"username": "lisa_anderson", "first_name": "Lisa", "last_name": "Anderson", "gender": "Female"},
    {"username": "chris_thompson", "first_name": "Chris", "last_name": "Thompson", "gender": "Male"},
    {"username": "amanda_white", "first_name": "Amanda", "last_name": "White", "gender": "Female"},
    {"username": "james_martinez", "first_name": "James", "last_name": "Martinez", "gender": "Male"},
    {"username": "olivia_garcia", "first_name": "Olivia", "last_name": "Garcia", "gender": "Female"},
    {"username": "robert_rodriguez", "first_name": "Robert", "last_name": "Rodriguez", "gender": "Male"},
    {"username": "sophia_lee", "first_name": "Sophia", "last_name": "Lee", "gender": "Female"},
    {"username": "danah_test", "first_name": "Danah", "last_name": "Alsayyari", "gender": "Female"},
]

db = SessionLocal()
created = 0
skipped = 0

for user_data in users_data:
    try:
        payload = UserCreate(**user_data)
        auth_service.register_user(db, payload)
        print(f"Created: {user_data['username']}")
        created += 1
    except ValueError as e:
        print(f"Skipped: {user_data['username']} - {e}")
        skipped += 1
    except Exception as e:
        print(f"Error: {user_data['username']} - {e}")

db.close()
print(f"\nDone! Created: {created}, Skipped: {skipped}")