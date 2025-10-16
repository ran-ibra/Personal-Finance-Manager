"""
main.py
---------
Personal Finance Manager (Console Version)
Handles the main menus and ties together:
- UserManager (user login & registration)
- TransactionManager (transactions)
- ReportsManager (reports and summaries)
"""

import sys
from users import UserManager
from transactions import TransactionManager
from reports import ReportsManager


# -----------------------------
# Helper UI functions
# -----------------------------


def pause():
    input("\nPress Enter to continue...")

def print_header(title: str):
    user = user_manager.get_current_user()
    name_display = f"👤 {user}" if user else " Not logged in"
    print("\n" + "=" * 60)
    print(f"{title.center(60)}")
    print("=" * 60)
    print(f"{name_display}\n" + "-" * 60)
# -----------------------------
# Initialize Managers
# -----------------------------
user_manager = UserManager()
transaction_manager = TransactionManager()
reports_manager = ReportsManager(transaction_manager)


if user_manager.get_current_user():
    print(f"✅ Welcome back, {user_manager.get_current_user()}! You are already logged in.\n")


# -----------------------------
# Menus
# -----------------------------
def main_menu():
    """Main entry menu"""
    while True:
        print_header("PERSONAL FINANCE MANAGER")
        print("1. User Management")
        print("2. Transactions")
        print("3. Reports")
        print("4. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            user_menu()
        elif choice == "2":
            transaction_menu()
        elif choice == "3":
            report_menu()
        elif choice == "4":
            print("👋 Goodbye! Have a great day.")
            sys.exit(0)
        else:
            print(" Invalid choice.")
            pause()


def user_menu():
    """Handles user-related options"""
    while True:
        print_header("USER MANAGEMENT")
        print("1. Register User")
        print("2. Login User")
        print("3. Logout")
        print("4. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            success, msg = user_manager.register_user(username, password)
            print(msg)

        elif choice == "2":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            success, msg = user_manager.login(username, password)
            print(msg)

        elif choice == "3":
            user_manager.logout()
            print("Logged out successfully.")

        elif choice == "4":
            return
        else:
            print("Invalid choice.")
        pause()


def transaction_menu():
    """Handles transaction-related options"""
    if not user_manager.get_current_user():
        print("⚠️  Please log in first.")
        pause()
        return

    username = user_manager.get_current_user()
    while True:
        print_header("💳 TRANSACTIONS")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Edit Transaction")
        print("4. Delete Transaction")
        print("5. Search Transactions")
        print("6. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            try:
                amount = float(input("Enter amount: "))
                category = input("Enter category: ").strip()
                description = input("Enter description: ").strip()
                t_type = input("Type (income/expense): ").strip().lower()

                txn = transaction_manager.add_transaction(
                    username, amount, category, description, t_type
                )
                print(f" Transaction added: {txn['id']} ({txn['type']})")

                # Update user balance
                if t_type == "income":
                    user_manager.update_balance(username, amount)
                elif t_type == "expense":
                    user_manager.update_balance(username, -amount)

            except ValueError:
                print(" Invalid amount. Must be a number.")

        elif choice == "2":
            txns = transaction_manager.get_user_transactions(username)
            if not txns:
                print("📭 No transactions found.")
            else:
                print("\nID | TYPE | AMOUNT | CATEGORY | DATE | DESCRIPTION")
                print("-" * 70)
                for t in txns:
                    print(
                        f"{t['id']:>2} | {t['type']:<7} | {t['amount']:>8.2f} | "
                        f"{t['category']:<10} | {t['date']:<19} | {t['description']}"
                    )

        elif choice == "3":
            txn_id = input("Enter transaction ID to edit: ").strip()
            updates = {}
            new_category = input("New category (leave blank to keep): ").strip()
            new_desc = input("New description (leave blank to keep): ").strip()
            new_amount = input("New amount (leave blank to keep): ").strip()
            if new_category:
                updates["category"] = new_category
            if new_desc:
                updates["description"] = new_desc
            if new_amount:
                try:
                    updates["amount"] = float(new_amount)
                except ValueError:
                    print(" Invalid amount.")
            updated = transaction_manager.edit_transaction(int(txn_id), updates)
            print("✅ Transaction updated." if updated else " Transaction not found.")

        elif choice == "4":
            txn_id = input("Enter transaction ID to delete: ").strip()
            deleted = transaction_manager.delete_transaction(int(txn_id))
            print("✅ Transaction deleted." if deleted else " Transaction not found.")

        elif choice == "5":
            cat = input("Category (optional): ").strip() or None
            start = input("Start date (YYYY-MM-DD) optional: ").strip() or None
            end = input("End date (YYYY-MM-DD) optional: ").strip() or None
            results = transaction_manager.search_transactions(username, cat, start, end)
            if not results:
                print("🔍 No matching transactions found.")
            else:
                for t in results:
                    print(f"{t['date']} | {t['category']} | {t['type']} | {t['amount']:.2f} | {t['description']}")

        elif choice == "6":
            return
        else:
            print(" Invalid choice.")
        pause()


def report_menu():
    """Handles reports and summaries"""
    if not user_manager.get_current_user():
        print("  Please log in first.")
        pause()
        return

    username = user_manager.get_current_user()
    while True:
        print_header("REPORTS & DASHBOARD")
        print("1. Dashboard Summary")
        print("2. Monthly Report")
        print("3. Category Breakdown")
        print("4. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            summary = reports_manager.dashboard_summary(username)
            reports_manager.print_report("Dashboard Summary", summary)

        elif choice == "2":
            month = input("Enter month (YYYY-MM): ").strip()
            summary = reports_manager.monthly_report(username, month)
            reports_manager.print_report(f"Monthly Report for {month}", summary)

        elif choice == "3":
            breakdown = reports_manager.category_breakdown(username)
            reports_manager.print_report("Category Breakdown", breakdown)

        elif choice == "4":
            return
        else:
            print(" Invalid choice.")
        pause()


# -----------------------------
# Program Entry
# -----------------------------
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n Exiting... Goodbye!")
        sys.exit(0)
            