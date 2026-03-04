# main.py

from atm_app.customer import customer_menu
from atm_app.admin import admin_menu
from atm_app.utils import clear_screen, pause

def main_menu():
    from atm_app.admin_smartcard_login import auto_admin_card_check

    while True:

        #CARD LOGIN
        if auto_admin_card_check():
            continue

        clear_screen()
        print("===== ATM SIMULATOR =====")
        print("1. Customer login")
        print("2. Admin login")
        print("3. Exit")

        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Please enter a valid number.")
            pause()
            continue

        #CUSTOMER LOGIN 
        if choice == 1:
            customer_menu()

        #ADMIN LOGIN 
        elif choice == 2:
            print("\nAdmin Login:")
            print("Insert your Admin Smart Card OR enter PIN.")

            from atm_app.admin_smartcard_login import read_admin_card, ADMIN_SMARTCARD_ID
            atr = read_admin_card()

            if atr == ADMIN_SMARTCARD_ID:
                print(" Admin Smart Card Verified!")
                pause()
                admin_menu()
            else:
                print("\nSmart card not detected or invalid.")
                pwd = input("Enter admin password: ")

                if pwd == "admin123":
                    admin_menu()
                else:
                    print("Invalid admin password!")
                    pause()

        elif choice == 3:
            print("Thank you for using the ATM.")
            break

        else:
            print("Invalid choice.")
            pause()


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nATM shutdown by user (Ctrl+C). Goodbye!")
