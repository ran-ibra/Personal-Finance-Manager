import json
import csv
import os
import bcrypt
from typing import Dict, List, Tuple
from datetime import datetime

# Custom exceptions
class DataError(Exception):
    """Base class for data handling errors"""
    pass

class FileAccessError(DataError):
    """Raised when there are issues accessing data files"""
    pass

class DataValidationError(DataError):
    """Raised when data validation fails"""
    pass

# File paths
USERS_FILE = "users.json"
TRANSACTIONS_FILE = "transactions.csv"

# Password handling
def hash_password(password: str) -> bytes:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except (ValueError, TypeError):
        return False

def load_users() -> Dict:
    """Load users from JSON file"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                data = json.load(f)
                # Validate data structure
                if not isinstance(data, dict):
                    raise DataValidationError("Invalid users data format")
                return data
        return {}
    except json.JSONDecodeError as e:
        raise FileAccessError(f"Error decoding users file: {str(e)}")
    except IOError as e:
        raise FileAccessError(f"Error reading users file: {str(e)}")

def save_users(users: Dict) -> None:
    """Save users to JSON file"""
    try:
        if not isinstance(users, dict):
            raise DataValidationError("Invalid users data type")
        
        # Safely create directory only if path includes one
        directory = os.path.dirname(USERS_FILE)
        if directory:  # avoid error if USERS_FILE is in current folder
            os.makedirs(directory, exist_ok=True)
        
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)
    except IOError as e:
        raise FileAccessError(f"Error saving users file: {str(e)}")
    except TypeError as e:
        raise DataValidationError(f"Error serializing users data: {str(e)}")

def load_transactions() -> List[Dict]:
    """Load transactions from CSV file"""
    try:
        transactions = []
        if os.path.exists(TRANSACTIONS_FILE):
            with open(TRANSACTIONS_FILE, 'r') as f:
                reader = csv.DictReader(f)
                transactions = list(reader)
                
                # Validate transaction data
                required_fields = {'id', 'user', 'amount', 'category', 'type', 'date'}
                for transaction in transactions:
                    missing_fields = required_fields - set(transaction.keys())
                    if missing_fields:
                        raise DataValidationError(
                            f"Transaction missing required fields: {missing_fields}")
                    
                    # Convert amount to float
                    try:
                        transaction['amount'] = float(transaction['amount'])
                    except ValueError:
                        raise DataValidationError(
                            f"Invalid amount in transaction {transaction['id']}")
                        
        return transactions
    except csv.Error as e:
        raise FileAccessError(f"Error reading transactions file: {str(e)}")
    except IOError as e:
        raise FileAccessError(f"Error accessing transactions file: {str(e)}")

def save_transactions(transactions: List[Dict]) -> None:
    """Save transactions to CSV file"""
    try:
        if not transactions:
            return
            
        if not isinstance(transactions, list):
            raise DataValidationError("Transactions must be a list")
            
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(TRANSACTIONS_FILE), exist_ok=True)
        
        fieldnames = transactions[0].keys()
        with open(TRANSACTIONS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transactions)
    except csv.Error as e:
        raise FileAccessError(f"Error writing transactions file: {str(e)}")
    except IOError as e:
        raise FileAccessError(f"Error accessing transactions file: {str(e)}")
    except AttributeError as e:
        raise DataValidationError(f"Invalid transaction data format: {str(e)}")

def validate_transaction(transaction: Dict) -> bool:
    """Validate a single transaction"""
    required_fields = {'user', 'amount', 'category', 'type', 'description'}
    
    # Check required fields
    if not all(field in transaction for field in required_fields):
        return False
        
    # Validate amount
    try:
        float(transaction['amount'])
    except (ValueError, TypeError):
        return False
        
    # Validate date if present
    if 'date' in transaction:
        try:
            datetime.strptime(transaction['date'], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return False
            
    return True

def load_data() -> Tuple[Dict, List[Dict]]:
    """Load both users and transactions data"""
    try:
        users = load_users()
        transactions = load_transactions()
        return users, transactions
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
