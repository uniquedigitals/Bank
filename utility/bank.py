class Bank:
    def __init__(self, name, account_number, pin="0000", balance=100, credit_limit=100000):
        self.name = name
        self.account_number = str(account_number)
        self.balance = float(balance)
        self.pin = str(pin)
        self.credit_limit = float(credit_limit)

    def info(self):
        data = {
            "name": self.name,
            "account_number": self.account_number,
            "balance": f"${self.balance:.2f}",
            "credit_limit": f"${self.credit_limit:.2f}",
        }
        for key, value in data.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

    def check_balance(self):
        print(f"Your current balance is ${self.balance:.2f}")

    def deposit(self):
        try:
            amount = float(input("Enter amount to deposit: "))
            if amount <= 0:
                print("Invalid amount. Must be greater than 0.")
                return

            self.balance += amount
            self.credit_limit += amount / 10
            print(f"${amount:.2f} deposited successfully.")
            self.check_balance()
        except ValueError:
            print("Invalid input! Please enter a valid numerical amount.")

    def withdraw(self):
        try:
            amount = float(input("Enter amount to withdraw: "))
            if amount <= 0:
                print("Invalid amount. Must be greater than 0.")
                return
            if amount > self.balance:
                print("Insufficient balance.")
                return

            self.balance -= amount
            self.credit_limit -= amount / 10
            print(f"${amount:.2f} withdrawn successfully.")
            self.check_balance()
        except ValueError:
            print("Invalid input! Please enter a valid numerical amount.")

    def transfer(self):
        try:
            amount = float(input("Enter amount to transfer: "))
            if amount <= 0:
                print("Invalid amount.")
                return
            if amount > self.balance:
                print("Insufficient funds for this transfer.")
                return

            target_number = input("Enter destination account number: ").strip()

            if target_number == self.account_number:
                print("You cannot transfer money to your own account.")
                return

            target_account = None
            for acc in accounts:
                if acc.account_number == target_number:
                    target_account = acc
                    break

            if target_account:
                self.balance -= amount
                target_account.balance += amount
                print(
                    f"${amount:.2f} transferred successfully to Account: {target_account.account_number} ({target_account.name})")
                self.check_balance()
            else:
                print("Account number not found.")
        except ValueError:
            print("Invalid input! Please enter a valid numerical amount.")

    def cancel(self):
        print("\nThank you for using Our Bank. Goodbye!")
        exit()

    def menu(self):
        options = {
            '1': ['Account Info', self.info],
            '2': ['Check Balance', self.check_balance],
            '3': ['Deposit', self.deposit],
            '4': ['Withdraw', self.withdraw],
            '5': ['Transfer', self.transfer],
            '0': ['Logout', self.cancel]
        }

        print(f"\n=== Welcome, {self.name} ===")
        for key, value in options.items():
            print(f"[{key}] {value[0]}")

        choice = input("Select an option: ").strip()

        if choice in options:
            options[choice][1]()
        else:
            print("Invalid selection. Please try again.")


# Account database setup
tolu = Bank("Tolu Ademola", "123456", pin="1234", balance=600)
sola = Bank("Sola Ilesanmi", "23456", pin="1224", balance=800)
samuel = Bank("Samuel Olaide", "123446", pin="1334", balance=100)

accounts = [tolu, sola, samuel]