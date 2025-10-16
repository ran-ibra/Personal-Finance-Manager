"""
users.py
---------
Implements user registration, login, and profile switching
using models.User and data_manager.
"""

import hashlib
from typing import Optional
from models import User
from data import load_data, save_data, USERS_FILE


class UserManager:
    """Handles all user-related functionality."""

    def __init__(self):
        self.users: list[User] = []
        self.current_user: Optional[User] = None
        self.load_users()

    # -----------------------------
    # Utility Methods
    # -----------------------------
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def load_users(self):
        """Load all users from users.json."""
        data = load_data(USERS_FILE)
        self.users = [User.from_dict(u) for u in data]

    def save_users(self):
        """Save all users to users.json."""
        save_data(USERS_FILE, [u.to_dict() for u in self.users])

    def find_user(self, name: str) -> Optional[User]:
        """Find user by username (case-insensitive)."""
        for user in self.users:
            if user.name.lower() == name.lower():
                return user
        return None

    # -----------------------------
    # Core Functionalities
    # -----------------------------
    def register_user(self):
        """Register a new user with hashed password."""
        print("\n--- Register New User ---")
        username = input("Enter your name: ").strip()

        if not username:
            print("❌ Username cannot be empty.")
            return

        if self.find_user(username):
            print("❌ Username already exists.")
            return

        password = input("Create a password: ").strip()
        confirm = input("Confirm password: ").strip()

        if password != confirm:
            print("❌ Passwords do not match.")
            return

        currency = input("Preferred currency (e.g., USD, EUR): ").strip().upper() or "USD"
        hashed_pw = self.hash_password(password)

        new_user = User.create(username, hashed_pw, currency)
        self.users.append(new_user)
        self.save_users()

        print(f"✅ User '{username}' registered successfully!")

    def login_user(self):
        """Log in existing user by verifying password."""
        print("\n--- User Login ---")
        if not self.users:
            print("⚠️ No users found. Please register first.")
            return None

        username = input("Enter your name: ").strip()
        password = input("Enter your password: ").strip()

        user = self.find_user(username)
        if not user:
            print("❌ No such user found.")
            return None

        if user.password == self.hash_password(password):
            self.current_user = user
            print(f"✅ Welcome back, {user.name}!")
            return user
        else:
            print("❌ Incorrect password.")
            return None

    def switch_user(self):
        """Switch between existing profiles."""
        print("\n--- Switch User ---")
        if not self.users:
            print("⚠️ No users available.")
            return None

        for i, user in enumerate(self.users, start=1):
            marker = "👤" if self.current_user and user.user_id == self.current_user.user_id else " "
            print(f"{i}. {marker} {user.name} ({user.currency})")

        choice = input("\nSelect user number (or press Enter to cancel): ").strip()
        if not choice:
            print("🔙 Cancelled.")
            return None

        try:
            index = int(choice) - 1
            if 0 <= index < len(self.users):
                self.current_user = self.users[index]
                print(f"🔁 Switched to {self.current_user.name}")
                return self.current_user
            else:
                print("❌ Invalid selection.")
                return None
        except ValueError:
            print("❌ Please enter a valid number.")
            return None
