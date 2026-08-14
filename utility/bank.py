class Bank:
    def __init__(self, name, account_number, pin="0000", balance=100.0, credit_limit=100000.0):
        self.name = name
        self.account_number = str(account_number)
        self.balance = float(balance)
        self.pin = str(pin)
        self.credit_limit = float(credit_limit)

    def deposit(self, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                return False, "Invalid amount. Must be greater than $0.00."

            self.balance += amount
            self.credit_limit += amount / 10
            return True, f"${amount:.2f} deposited successfully."
        except (ValueError, TypeError):
            return False, "Invalid input! Please enter a valid numerical amount."

    def withdraw(self, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                return False, "Invalid amount. Must be greater than $0.00."
            if amount > self.balance:
                return False, "Insufficient balance."

            self.balance -= amount
            self.credit_limit -= amount / 10
            return True, f"${amount:.2f} withdrawn successfully."
        except (ValueError, TypeError):
            return False, "Invalid input! Please enter a valid numerical amount."

    def transfer(self, amount, target_number, accounts_list):
        try:
            amount = float(amount)
            if amount <= 0:
                return False, "Invalid amount."
            if amount > self.balance:
                return False, "Insufficient funds for this transfer."

            target_number = str(target_number).strip()

            if target_number == self.account_number:
                return False, "You cannot transfer money to your own account."

            target_account = next((acc for acc in accounts_list if acc.account_number == target_number), None)

            if target_account:
                self.balance -= amount
                target_account.balance += amount
                return True, f"${amount:.2f} transferred successfully to {target_account.name} ({target_account.account_number})."
            else:
                return False, "Destination account number not found."
        except (ValueError, TypeError):
            return False, "Invalid input! Please enter a valid numerical amount."


# Account database setup
tolu = Bank("Tolu Ademola", "123456", pin="1234", balance=600)
sola = Bank("Sola Ilesanmi", "23456", pin="1224", balance=800)
samuel = Bank("Samuel Olaide", "123446", pin="1334", balance=100)

accounts = [tolu, sola, samuel]