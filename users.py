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
        """Register a new user"""
        try:
            if not username or not password:
                return False, "Username and password are required"
                
            if username in self.users:
                return False, "Username already exists"
            
            # Hash the password before storing
            hashed_password = hash_password(password)
            
            self.users[username] = {
                "password": hashed_password.decode('utf-8'),  # Store as string
                "balance": 0.0
            }
            save_users(self.users)
            return True, "User registered successfully"
            
        except DataError as e:
            return False, f"Registration failed: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error during registration: {str(e)}"

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """Login a user"""
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
        """Logout current user"""
        self.current_user = None

    def get_user_balance(self, username: str) -> float:
        """Get user's current balance"""
        if username in self.users:
            return self.users[username]["balance"]
        return 0.0

    def update_balance(self, username: str, amount: float) -> None:
        """Update user's balance"""
        if username in self.users:
            self.users[username]["balance"] += amount
            save_users(self.users)

    def get_current_user(self) -> Optional[str]:
        """Get current logged in user"""
        return self.current_user


#####testiinggg temmpooraarryy###
if __name__ == "__main__":
    manager = UserManager()
    print(manager.register_user("hager", "1234"))
    print(manager.login("hager", "1234"))
    print(manager.register_user("rana", "1234"))
    print(manager.login("rana", "1234"))
