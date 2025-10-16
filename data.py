import json
import csv
import os
from typing import List, Dict, Any

# File paths
USERS_FILE = "data/users.json"
TRANSACTIONS_FILE = "data/transactions.csv"

def load_data(file_path: str) -> List[Dict[str, Any]]:
    """Load data from a JSON file (for users)."""
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            json.dump([], f)
        return []

    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_data(file_path: str, data: List[Dict[str, Any]]):
    """Save data to a JSON file (for users)."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------
# CSV Handling (Transactions)
# -----------------------------
def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Load all transactions from CSV file."""
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "transaction_id", "user_id", "type", "amount", "category",
                "date", "description", "payment_method"
            ])
        return []

    transactions = []
    with open(file_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append(row)
    return transactions


def save_transactions(file_path: str, transactions: List[Dict[str, Any]]):
    """Save transactions list to CSV file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    fieldnames = [
        "transaction_id", "user_id", "type", "amount",
        "category", "date", "description", "payment_method"
    ]

    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transactions)
