# atm_app/customer.py

from atm_app.account import Account
from atm_app.utils import (
    ACCOUNTS_FILE,
    TXN_FILE,
    load_json,
    save_json,
    log_transaction,
    clear_screen,
    pause,
)
from atm_app.utils import load_accounts, save_accounts



# LOGIN USING ACCOUNT NUMBER + PIN

def customer_login() -> Account | None:
    accounts = load_accounts()
    acc_no = input("Enter account number: ")
    pin = input("Enter PIN: ")

    acc = accounts.get(acc_no)

    if acc is None:
        print("Account not found.")
        pause()
        return None

    if acc.pin != pin:
        print("Invalid PIN.")
        pause()
        return None

    return acc


# TRANSACTION HISTORY

def view_transaction_history(acc_no):
    transactions = load_json(TXN_FILE, [])

    print("\n===== TRANSACTION HISTORY =====")
    print("DATE & TIME\t\tTYPE\t\tAMOUNT")
    print("--------------------------------------------")

    found = False

    for tx in transactions:
        if tx.get("acc_no") == acc_no:
            found = True
            amount = f"+{tx['amount']}" if tx["amount"] > 0 else f"{tx['amount']}"
            time_str = tx.get("time", "NO-TIME")
            print(f"{time_str}\t{tx['type']}\t\t{amount}")

    if not found:
        print("No transactions found for this account.")

    print("--------------------------------------------")
    pause()


# PRINT RECEIPT
def print_receipt(acc, tx_type, amount):
    from datetime import datetime
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sign = "+" if tx_type == "DEPOSIT" else "-"
    amt_display = f"{sign}{abs(amount):.2f}"

    print("\n========================================")
    print("              ATM RECEIPT               ")
    print("----------------------------------------")
    print(f"Account No : {acc.acc_no}")
    print(f"Name       : {acc.name}")
    print(f"Transaction: {tx_type}")
    print(f"Amount     : {amt_display}")
    print(f"Date/Time  : {time_now}")
    print(f"Balance    : {acc.balance:.2f}")
    print("========================================")
    pause()


# CUSTOMER MENU

def customer_menu(acc=None):
    if acc is None:
        acc = customer_login()

    if not acc:
        return

    while True:
        clear_screen()
        print(f"===== CUSTOMER MENU ({acc.name}, Acc: {acc.acc_no}) =====")
        print("1. Check balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. View Transaction History")
        print("5. Logout")

        choice = input("Enter choice: ")

        accounts = load_accounts()
        acc = accounts[acc.acc_no]  # refresh latest state

        # BALANCE 
        if choice == "1":
            print(f"Current balance: {acc.balance:.2f}")
            pause()

        # DEPOSIT 
        elif choice == "2":
            amount_input = input("Enter amount to deposit: ").strip()

            if not amount_input.replace(".", "", 1).isdigit():
                print("Invalid amount.")
                pause()
                continue

            amount = float(amount_input)

            if amount <= 0:
                print("Amount must be positive.")
                pause()
                continue

            if acc.deposit(amount):
                accounts[acc.acc_no] = acc
                save_accounts(accounts)
                log_transaction(acc.acc_no, amount, "DEPOSIT")
                print("Deposit successful.")
                print_receipt(acc, "DEPOSIT", amount)
            else:
                print("Deposit failed.")
                pause()

        # WITHDRAW
        elif choice == "3":
            amount_input = input("Enter amount to withdraw: ").strip()

            if not amount_input.replace(".", "", 1).isdigit():
                print("Invalid amount. Please enter a numeric value.")
                pause()
                continue

            amount = float(amount_input)

            if amount <= 0:
                print("Amount must be greater than 0.")
                pause()
                continue

            if amount > acc.balance:
                print(f"Insufficient balance! You only have {acc.balance:.2f} available.")
                pause()
                continue

            if acc.withdraw(amount):
                accounts[acc.acc_no] = acc
                save_accounts(accounts)
                log_transaction(acc.acc_no, -amount, "WITHDRAW")
                print("Withdrawal successful.")
                print_receipt(acc, "WITHDRAW", amount)
            else:
                print("Withdrawal failed.")
                pause()

        # HISTORY
        elif choice == "4":
            view_transaction_history(acc.acc_no)

        # LOGOUT 
        elif choice == "5":
            print("Logging out...")
            pause()
            break

        else:
            print("Invalid choice.")
            pause()
