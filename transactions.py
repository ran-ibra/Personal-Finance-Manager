
from typing import List, Optional
from dataclasses import asdict
from models import Transaction
from data import load_transactions, save_transactions, TRANSACTIONS_FILE
import uuid


class TransactionManager:
    """Manages all income and expense transactions."""

    def __init__(self, current_user_id: Optional[str] = None):
        self.current_user_id = current_user_id
        self.transactions: List[Transaction] = []
        self.load_all_transactions()

    # -----------------------------
    # Persistence
    # -----------------------------
    def load_all_transactions(self):
        """Load all transactions from CSV."""
        data = load_transactions(TRANSACTIONS_FILE)
        self.transactions = [Transaction.from_dict(t) for t in data]

    def save_all_transactions(self):
        """Save all transactions back to CSV."""
        save_transactions(TRANSACTIONS_FILE, [t.to_dict() for t in self.transactions])

    # -----------------------------
    # CRUD Functions
    # -----------------------------
    def add_transaction(self):
        """Add a new transaction for the current user."""
        if not self.current_user_id:
            print(" Please log in first.")
            return

        print("\n--- Add Transaction ---")
        t_type = input("Type (income/expense): ").strip().lower()
        if t_type not in ["income", "expense"]:
            print(" Invalid type.")
            return

        try:
            amount = float(input("Amount: ").strip())
        except ValueError:
            print(" Invalid amount.")
            return

        category = input("Category (e.g., Food, Rent, Salary): ").strip().title()
        description = input("Description: ").strip()
        payment_method = input("Payment Method (Cash, Credit Card, etc.): ").strip().title()

        new_txn = Transaction.create(
            user_id=self.current_user_id,
            type=t_type,
            amount=amount,
            category=category,
            description=description,
            payment_method=payment_method,
        )

        self.transactions.append(new_txn)
        self.save_all_transactions()

        print(f"✅ {t_type.capitalize()} of {amount:.2f} added successfully!")

    def view_transactions(self):
        """Display all transactions for the current user."""
        if not self.current_user_id:
            print("⚠️  Please log in first.")
            return

        print("\n--- Your Transactions ---")
        user_txns = [t for t in self.transactions if t.user_id == self.current_user_id]

        if not user_txns:
            print("📭 No transactions found.")
            return

        print(f"{'ID':<10} {'TYPE':<10} {'AMOUNT':<10} {'CATEGORY':<15} {'DATE':<12} {'PAYMENT':<15} DESCRIPTION")
        print("-" * 80)
        for t in user_txns:
            print(
                f"{t.transaction_id:<10} {t.type:<10} {t.amount:<10.2f} "
                f"{t.category:<15} {t.date:<12} {t.payment_method:<15} {t.description}"
            )

    def edit_transaction(self):
        """Edit an existing transaction."""
        if not self.current_user_id:
            print("  Please log in first.")
            return

        self.view_transactions()
        txn_id = input("\nEnter Transaction ID to edit (e.g., TXN-ABC123): ").strip().upper()

        for t in self.transactions:
            if t.transaction_id.upper() == txn_id and t.user_id == self.current_user_id:
                print("\n--- Editing Transaction ---")
                t.category = input(f"New category [{t.category}]: ").strip() or t.category
                t.description = input(f"New description [{t.description}]: ").strip() or t.description
                t.payment_method = input(f"New payment method [{t.payment_method}]: ").strip() or t.payment_method

                try:
                    new_amount = input(f"New amount [{t.amount}]: ").strip()
                    if new_amount:
                        t.amount = float(new_amount)
                except ValueError:
                    print(" Invalid amount, keeping previous value.")

                self.save_all_transactions()
                print("Transaction updated successfully!")
                return

        print(" Transaction not found.")

    def delete_transaction(self):
        """Delete a transaction by ID."""
        if not self.current_user_id:
            print("Please log in first.")
            return

        self.view_transactions()
        txn_id = input("\nEnter Transaction ID to delete: ").strip().upper()

        for t in self.transactions:
            if t.transaction_id.upper() == txn_id and t.user_id == self.current_user_id:
                confirm = input(f"Are you sure you want to delete {txn_id}? (y/n): ").strip().lower()
                if confirm == "y":
                    self.transactions.remove(t)
                    self.save_all_transactions()
                    print("✅ Transaction deleted successfully!")
                else:
                    print("🔙 Cancelled.")
                return

        print(" Transaction not found.")

    def search_transactions(self):
        """Search transactions by category or description."""
        if not self.current_user_id:
            print("  Please log in first.")
            return

        keyword = input("\nEnter keyword to search (category/description): ").strip().lower()
        matches = [
            t for t in self.transactions
            if t.user_id == self.current_user_id and
            (keyword in t.category.lower() or keyword in t.description.lower())
        ]

        if not matches:
            print(" No matches found.")
            return

        print("\n--- Search Results ---")
        for t in matches:
            print(f"{t.transaction_id}: {t.type.capitalize()} {t.amount:.2f} ({t.category}) on {t.date}")
