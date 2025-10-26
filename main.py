import getpass

import sys
from users import UserManager
from transactions import TransactionManager
from reports import ReportsManager
from datetime import datetime
from datetime import datetime
from advancedFeatures import AdvancedFeatures


def pause():
    input("\nPress Enter to continue...")

def print_header(title: str):
    user = user_manager.get_current_user()
    name_display = f"👤 {user}" if user else " Not logged in"
    print("\n" + "=" * 60)
    print(f"{title.center(60)}")
    print("=" * 60)
    print(f"{name_display}\n" + "-" * 60)

user_manager = UserManager()
transaction_manager = TransactionManager()
reports_manager = ReportsManager(transaction_manager)
advanced_features = AdvancedFeatures(transaction_manager)

if user_manager.get_current_user():
    print(f"✅ Welcome back, {user_manager.get_current_user()}! You are already logged in.\n")



def main_menu():
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
            print(" Goodbye! Have a great day.")
            sys.exit(0)
        else:
            print(" Invalid choice.")
            pause()


def user_menu():

    while True:
        print_header("USER MANAGEMENT")
        print("1. Register User")
        print("2. Login User")
        print("3. Switch User")
        print("4. Logout")
        print("5. View Profile")
        print("6. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            success, msg = user_manager.register_user(username, password)
            print(msg)
        elif choice == "2":
            username = input("Enter username: ").strip()
            # password = input("Enter password: ").strip()
            password = getpass.getpass("Enter password: ").strip()
            success, msg = user_manager.login(username, password)
            print(msg)
        elif choice == "3":
            user_manager.logout()
            username = input("Enter switched username: ").strip()
            # password = input("Enter password: ").strip()
            password = getpass.getpass("Enter password: ").strip()
            success, msg = user_manager.login(username, password)
            print(msg)

        elif choice == "4":
            user_manager.logout()
            print("Logged out successfully.")
        elif choice == "5":
            profile= user_manager.get_user_profile()
            if not profile:
                print("No user logged in or user not found.")
            else:
                print("\nUSER PROFILE")
                print("-" * 20)
                print(f"Username : {profile['username']}")
                print(f"Balance  : {profile['balance']:.2f}")
                


        elif choice == "6":
            return
        else:
            print("Invalid choice.")
        pause()


def transaction_menu():
    if not user_manager.get_current_user():
        print("  Please log in first.")
        pause()
        return

    username = user_manager.get_current_user()
    while True:
        print_header("TRANSACTIONS")
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
                print("No transactions found.")
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
            print("Transaction updated." if updated else " Transaction not found.")

        elif choice == "4":
            txn_id = input("Enter transaction ID to delete: ").strip()
            deleted = transaction_manager.delete_transaction(int(txn_id))
            print("Transaction deleted." if deleted else " Transaction not found.")

        elif choice == "5":
            cat = input("Category (optional): ").strip() or None
            start = input("Start date (YYYY-MM-DD) optional: ").strip() or None
            end = input("End date (YYYY-MM-DD) optional: ").strip() or None
            results = transaction_manager.search_transactions(username, cat, start, end)
            if not results:
                print(" No matching transactions found.")
            else:
                for t in results:
                    print(f"{t['date']} | {t['category']} | {t['type']} | {t['amount']:.2f} | {t['description']}")

        elif choice == "6":
            return
        else:
            print(" Invalid choice.")
        pause()

def report_menu():
    def _validate_month(month_str: str) -> bool:
        try:
            datetime.strptime(month_str, "%Y-%m")
            return True
        except Exception:
            return False

    if not user_manager.get_current_user():
        print(" Please log in first.")
        pause()
        return

    username = user_manager.get_current_user()
    while True:
        print_header("REPORTS & DASHBOARD")
        print("1. Dashboard Summary")
        print("2. Monthly Report")
        print("3. Category Breakdown")
        print("4. Financial Health Score")
        print("5. Monthly Budget")
        print("6. Manage Savings Goals")
        print("7. Manage Recurring Transactions")
        print("8. Back to Main Menu")


        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            data = reports_manager.dashboard_summary(username)
            if not data:
                print("No dashboard data available.")
            else:
                reports_manager.print_report("Dashboard Summary", data)

        elif choice == "2":
            month = input("Enter month (YYYY-MM): ").strip()
            if not _validate_month(month):
                print("Invalid month format. Expected YYYY-MM.")
            else:
                data = reports_manager.monthly_report(username, month)
                if not data:
                    print(f"No data for {month}.")
                else:
                    reports_manager.print_report(f"Monthly Report for {month}", data)

        elif choice == "3":
            data = reports_manager.category_breakdown(username)
            if not data:
                print("No category data available.")
            else:
                reports_manager.print_report("Category Breakdown", data)

        elif choice == "4":
            score = reports_manager.calculate_health_score(username)
            # Normalize numeric score into a simple report structure if needed
            if isinstance(score, (int, float)):
                reports_manager.print_report("Financial Health Score", {"score": score})
            elif score:
                reports_manager.print_report("Financial Health Score", score)
            else:
                print("Unable to calculate health score.")

        elif choice == "5":
            budget_submenu(username)
        elif choice == "6":
            savings_menu(username)
        elif choice == "7":
            recurring_menu(username)

        elif choice == "8":
            return

        else:
            print("Invalid choice.")
        pause()


def budget_submenu(username: str):

    def _validate_month(month_str: str) -> bool:
        try:
            datetime.strptime(month_str, "%Y-%m")
            return True
        except Exception:
            return False

    while True:
        print_header("MONTHLY BUDGET MANAGEMENT")
        print("1. Set Monthly Budget")
        print("2. View Budget Status")
        print("3. Back")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            month = input("Enter month (YYYY-MM): ").strip()
            if not _validate_month(month):
                print("Invalid month format. Expected YYYY-MM.")
            else:
                val = input("Enter budget limit: ").strip()
                try:
                    limit = float(val)
                    res = reports_manager.set_monthly_budget(username, month, limit)
                    if res is False:
                        print("Failed to set budget.")
                    else:
                        print(f"Budget set: {month} → {limit:.2f}")
                except ValueError:
                    print("Invalid number for budget limit.")

        elif choice == "2":
            month = input("Enter month (YYYY-MM): ").strip()
            if not _validate_month(month):
                print("Invalid month format. Expected YYYY-MM.")
            else:
                status = reports_manager.budget_status(username, month)
                if status is None:
                    print(f"No budget set for {month}.")
                else:
                    reports_manager.print_report(f"Budget Status for {month}", status)

        elif choice == "3":
            return

        else:
            print("Invalid choice.")
        pause()
def savings_menu(username: str):
    while True:
        print_header("SAVINGS GOALS")
        print("1. Add New Goal")
        print("2. View Goals")
        print("3. Back")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            name = input("Goal name: ").strip()
            try:
                target = float(input("Target amount: "))
                advanced_features.set_savings_goal(username, name, target)
            except ValueError:
                print("Invalid amount.")
        elif choice == "2":
            goals = advanced_features.get_savings_goals(username)
            for g_name, g_data in goals.items():
                print(f"\n🏁 {g_name}")
                for k, v in g_data.items():
                    print(f"  {k:<15}: {v}")
        elif choice == "3":
            return
        else:
            print("Invalid choice.")
        pause()


def recurring_menu(username: str):
    while True:
        print_header("RECURRING TRANSACTIONS")
        print("1. Add Recurring Transaction")
        print("2. View Recurring Transactions")
        print("3. Process Due Transactions")
        print("4. Back")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            try:
                amount = float(input("Amount: "))
                category = input("Category: ").strip()
                description = input("Description: ").strip()
                t_type = input("Type (income/expense): ").strip().lower()
                frequency = input("Frequency (daily/weekly/monthly): ").strip().lower()
                advanced_features.add_recurring_transaction(
                    username, amount, category, description, t_type, frequency
                )
            except ValueError:
                print("Invalid input.")
        elif choice == "2":
            recs = advanced_features.get_recurring_transactions(username)
            if not recs:
                print("No recurring transactions found.")
            else:
                for r in recs:
                    print(
                        f"{r['type'].capitalize()} ${r['amount']:,.2f} "
                        f"- {r['category']} ({r['frequency'].capitalize()} | Next: {r['next_date']})"
                    )
        elif choice == "3":
            advanced_features.process_recurring_transactions(username)
        elif choice == "4":
            return
        else:
            print("Invalid choice.")
        pause()



if __name__ == "__main__":
    try:
        class A:
            def method(self):
                print("A method")
            
        class B(A):
            def method(self):
                print("B method")
                

        class C(A):
            def method(self):
                print("C method")
               

        class D(B, C):
            def method(self):
                print("D method")
                super().method()
                

        d = D()
        d.method()
        main_menu()
    except KeyboardInterrupt:
        print("\n\n Exiting... Goodbye!")
        sys.exit(0)
            