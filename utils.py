
import json
import csv
import os
import bcrypt
from typing import Dict, List, Tuple
from datetime import datetime

# ---------- Exceptions ----------
class DataError(Exception):
    """Base class for data handling errors"""
    pass

class FileAccessError(DataError):
    """Raised when there are issues accessing data files"""
    pass

class DataValidationError(DataError):
    """Raised when data format/content is invalid"""
    pass

# ---------- File paths ----------
USERS_FILE = "users.json"
TRANSACTIONS_FILE = "transactions.csv"

# ---------- Users helpers ----------
def load_users() -> Dict:
    """Load users from JSON file; return {} if not exists"""
    try:
        if not os.path.exists(USERS_FILE):
            return {}
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                raise DataValidationError("Users file must contain a JSON object")
            return data
    except (json.JSONDecodeError, OSError) as e:
        raise FileAccessError(f"Error reading users file: {str(e)}")

def save_users(users: Dict) -> None:
    """Save users to JSON file"""
    try:
        if not isinstance(users, dict):
            raise DataValidationError("Invalid users data type")
        
        # Safely create directory only if path includes one
        directory = os.path.dirname(USERS_FILE)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
    except OSError as e:
        raise FileAccessError(f"Error saving users file: {str(e)}")
    except TypeError as e:
        raise DataValidationError(f"Error serializing users data: {str(e)}")

def hash_password(password: str) -> bytes:
    if not password:
        raise DataValidationError("Password is empty")
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(password: str, stored_hash: str) -> bool:
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode("utf-8")
    return bcrypt.checkpw(password.encode("utf-8"), stored_hash)

# ---------- Transactions helpers ----------
def load_transactions() -> List[Dict]:
    """Load transactions from CSV file"""
    try:
        transactions: List[Dict] = []
        if os.path.exists(TRANSACTIONS_FILE):
            with open(TRANSACTIONS_FILE, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Normalize fields
                    row["id"] = int(row.get("id", 0)) if row.get("id") else 0
                    row["user"] = row.get("user", "")
                    row["category"] = row.get("category", "")
                    row["description"] = row.get("description", "")
                    row["type"] = row.get("type", "").lower()
                    # amount & date
                    try:
                        row["amount"] = float(row.get("amount", 0.0))
                    except (TypeError, ValueError):
                        row["amount"] = 0.0
                    row["date"] = row.get("date") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    transactions.append(row)
        return transactions
    except (csv.Error, OSError) as e:
        raise FileAccessError(f"Error accessing transactions file: {str(e)}")

def save_transactions(transactions: List[Dict]) -> None:
    """Save transactions to CSV file"""
    try:
        fieldnames = ["id", "user", "amount", "category", "description", "type", "date"]
        with open(TRANSACTIONS_FILE, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for t in transactions:
                # ensure required keys exist
                row = {k: t.get(k, "") for k in fieldnames}
                writer.writerow(row)
    except (csv.Error, OSError) as e:
        raise FileAccessError(f"Error writing transactions file: {str(e)}")

# ---------- Combined helpers (optional) ----------
def load_data() -> Tuple[Dict, List[Dict]]:
    """Load both users and transactions data"""
    try:
        return load_users(), load_transactions()
    except (FileAccessError, DataValidationError) as e:
        # Log the error here if needed
        print(f"Error loading data: {str(e)}")
        return {}, []

def save_data(users: Dict, transactions: List[Dict]) -> bool:
    """Save both users and transactions data"""
    try:
        save_users(users)
        save_transactions(transactions)
        return True
    except (FileAccessError, DataValidationError) as e:
        # Log the error here if needed
        print(f"Error saving data: {str(e)}")
        return False
