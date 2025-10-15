from typing import Dict, List, Optional
from datetime import datetime
from utils import load_transactions, save_transactions

class TransactionManager:
    def __init__(self):
        self.transactions = load_transactions()

    def add_transaction(self, user: str, amount: float, category: str, description: str, 
                       transaction_type: str) -> Dict:
        """Add a new transaction"""
        transaction = {
            "id": len(self.transactions) + 1,
            "user": user,
            "amount": amount,
            "category": category,
            "description": description,
            "type": transaction_type,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.transactions.append(transaction)
        save_transactions(self.transactions)
        return transaction

    def get_user_transactions(self, username: str) -> List[Dict]:
        """Get all transactions for a specific user"""
        return [t for t in self.transactions if t["user"] == username]

    def get_transaction_by_id(self, transaction_id: int) -> Optional[Dict]:
        """Get a specific transaction by ID"""
        for transaction in self.transactions:
            if int(transaction["id"]) == transaction_id:
                return transaction
        return None

    def delete_transaction(self, transaction_id: int) -> bool:
        """Delete a transaction by ID"""
        for i, transaction in enumerate(self.transactions):
            if int(transaction["id"]) == transaction_id:
                self.transactions.pop(i)
                save_transactions(self.transactions)
                return True
        return False

    def edit_transaction(self, transaction_id: int, 
                        updates: Dict[str, str]) -> Optional[Dict]:
        """Edit an existing transaction"""
        for transaction in self.transactions:
            if int(transaction["id"]) == transaction_id:
                transaction.update(updates)
                save_transactions(self.transactions)
                return transaction
        return None

    def search_transactions(self, username: str, 
                          category: Optional[str] = None, 
                          start_date: Optional[str] = None,
                          end_date: Optional[str] = None) -> List[Dict]:
        """Search transactions with filters"""
        results = self.get_user_transactions(username)
        
        if category:
            results = [t for t in results if t["category"].lower() == category.lower()]
            
        if start_date:
            results = [t for t in results if t["date"] >= start_date]
            
        if end_date:
            results = [t for t in results if t["date"] <= end_date]
            
        return results
