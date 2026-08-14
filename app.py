from flask import Flask, render_template, request, redirect, url_for, session
from utility.bank import accounts

app = Flask(__name__)

print("=== BANK ATM SYSTEM ===")
user_acc_num = input('Enter your account number: ').strip()

    # 1. Search for matching account
user_account = None
for account in accounts:
    if account.account_number == user_acc_num:
        user_account = account
        break

    if not user_account:
        print("Account number not found!")
        exit()

    # 2. PIN Verification with 3 attempts
    attempts = 3
    authenticated = False

    while attempts > 0:
        entered_pin = input('Enter your PIN: ').strip()
        if entered_pin == user_account.pin:
            authenticated = True
            break
        else:
            attempts -= 1
            if attempts > 0:
                print(f"Incorrect PIN. You have {attempts} attempt(s) remaining.")

    # 3. Handle Fraud or Grant Access
    if not authenticated:
        print("\n[!] FRAUD DETECTED! Access Blocked.")
        exit()

    # 4. Continuous Menu Loop
    while True:
        user_account.menu()

if __name__ == '__main__':
    app.run()