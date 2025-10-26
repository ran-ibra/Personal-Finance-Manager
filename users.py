
import re
from typing import Dict, Optional, Tuple
from utils import (
    load_users, save_users, hash_password, verify_password,
    DataError, FileAccessError, DataValidationError
)

class UserManager:
    def __init__(self):
        self.users = load_users()
        self.current_user = None

    def register_user(self, username: str, password: str) -> Tuple[bool, str]:
        try:
            if not username or not password:
                return False, "Username and password are required"

            if username in self.users:
                return False, "Username already exists"

            #  Password regex validation
            pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@_#$%^&+=!]).{8,}$'
            if not re.match(pattern, password):
                return False, (
                    "Password must be at least 8 characters long, "
                    "contain at least one uppercase letter, one lowercase letter, "
                    "one number, and one special character (@, _, #, $, etc.)"
                )

            hashed_password = hash_password(password)
            
            self.users[username] = {
                "password": hashed_password.decode('utf-8'),
                "balance": 0.0
            }
            save_users(self.users)
            
            self.users = load_users()
            return True, "User registered successfully"

        except DataError as e:
            return False, f"Registration failed: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error during registration: {str(e)}"


    def login(self, username: str, password: str) -> Tuple[bool, str]:
        try:
            if not username or not password:
                return False, "Username and password are required"
                
            if username not in self.users:
                return False, "Invalid username or password"
                
            stored_password = self.users[username]["password"]
            
            if verify_password(password, stored_password):
                self.current_user = username
                return True, "Login successful"
            
            return False, "Invalid username or password"
            
        except DataError as e:
            return False, f"Login failed: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error during login: {str(e)}"

    def logout(self) -> None:
        self.current_user = None

    def get_user_balance(self, username: str) -> float:
        if username in self.users:
            return self.users[username]["balance"]
        return 0.0

    def update_balance(self, username: str, amount: float) -> None:
        if username in self.users:
            self.users[username]["balance"] += amount
            save_users(self.users)
    def get_user_profile(self, username: Optional[str] = None) -> Optional[Dict]:
        if username is None:
            username = self.current_user
        if not username:
            return None
        user = self.users.get(username)
        if not user:
            return None
        return {
            "username": username,
            "balance": float(user.get("balance", 0.0)),
        }

    def get_current_user(self) -> Optional[str]:
        return self.current_user

