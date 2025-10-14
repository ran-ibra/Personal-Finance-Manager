import sys

# da lma n3ml login aw haga h7tago 
current_user = None

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
        elif choice == "2":
            transaction_menu()
        elif choice == "3":
            report_menu()
        elif choice == "4":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")


def user_menu():
    print_header("haga tab3 el user ")
    #to register and login and switch user 
   


def transaction_menu():
    print_header(" TRANSACTIONS ")
    #add trans aw view el ta7wilat aw edit delelte search 
    


def report_menu():
    print_header("reports lsa hanshof btt3ml ezay ")
    # but we need to provide eh dashboard and monthly report and category breakdown 
    


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Goodbye!")
        sys.exit(0)
