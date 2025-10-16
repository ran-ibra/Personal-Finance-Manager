import sys
from users import UserManager
from transactions import TransactionManager

# da lma n3ml login aw haga h7tago 
current_user = None
user_manager = UserManager()
def print_header(title: str):
    print("\n" + "=" * 50)
    print(title.center(50))
    print("=" * 50)



def main_menu():
    while True:
        print_header("welcome")
        print("1. User Management")
        print("2. Transactions")
        print("3. Reports")
        print("4. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            user_menu()
        if choice == "2":  
            user = user_manager.login_user()
            if user:
                transaction_manager = TransactionManager(user.user_id)
                transaction_menu()
        elif choice == "3":
            report_menu()
        elif choice == "4":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")


def user_menu():
    print_header(" USER MANAGEMENT")
    print("1. Register User")
    print("2. Login User")
    print("3. Switch User")
    print("4. Back")

    choice = input("\nEnter your choice: ").strip()

    if choice == "1":
        user_manager.register_user()
    elif choice == "2":
        user_manager.login_user()
    elif choice == "3":
        user_manager.switch_user()
    elif choice == "4":
        return
    else:
        print(" Invalid choice.")
    


def transaction_menu():
    print_header(" TRANSACTIONS ")
    if not user_manager.current_user:
        print(" Please log in first.")

        return

    transaction_manager = TransactionManager(user_manager.current_user.user_id)

    while True:
        print_header("💳 TRANSACTION MANAGEMENT")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Edit Transaction")
        print("4. Delete Transaction")
        print("5. Search Transactions")
        print("6. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            transaction_manager.add_transaction()
        elif choice == "2":
            transaction_manager.view_transactions()
        elif choice == "3":
            transaction_manager.edit_transaction()
        elif choice == "4":
            transaction_manager.delete_transaction()
        elif choice == "5":
            transaction_manager.search_transactions()
        elif choice == "6":
            break
        else:
            print("Invalid choice.")


    


def report_menu():
    print_header("reports lsa hanshof btt3ml ezay ")
    # but we need to provide eh dashboard and monthly report and category breakdown 
    


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n Exiting... Goodbye!")
        sys.exit(0)
