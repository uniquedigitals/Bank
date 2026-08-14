from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utility.bank import accounts

# Create a Blueprint instance
bank_bp = Blueprint('bank', __name__)

# --- Helper Methods ---
def get_account_by_number(acc_num):
    for account in accounts:
        if account.account_number == str(acc_num):
            return account
    return None

def get_current_user():
    if 'user_account_num' not in session:
        return None
    return get_account_by_number(session['user_account_num'])

# --- Route Handlers ---

@bank_bp.route('/')
def index():
    user = get_current_user()
    if not user:
        return redirect(url_for('bank.login'))
    return render_template('index.html', account=user)


@bank_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        acc_num = request.form.get('account_number', '').strip()
        pin = request.form.get('pin', '').strip()

        account = get_account_by_number(acc_num)
        if not account:
            flash("Account number not found!", "danger")
            return redirect(url_for('bank.login'))

        attempts = session.get('attempts', 3)

        if account.pin == pin:
            session['user_account_num'] = account.account_number
            session.pop('attempts', None)
            flash(f"Welcome back, {account.name}!", "success")
            return redirect(url_for('bank.index'))
        else:
            attempts -= 1
            session['attempts'] = attempts

            if attempts <= 0:
                session.clear()
                flash("FRAUD DETECTED! Access Blocked due to multiple failed attempts.", "danger")
                return render_template('login.html', blocked=True)

            flash(f"Incorrect PIN. You have {attempts} attempt(s) remaining.", "warning")
            return redirect(url_for('bank.login'))

    return render_template('login.html', blocked=False)


@bank_bp.route('/check-balance')
def check_balance():
    user = get_current_user()
    if not user:
        return redirect(url_for('bank.login'))
    return render_template('check_balance.html', account=user)


@bank_bp.route('/deposit', methods=['GET', 'POST'])
def deposit():
    user = get_current_user()
    if not user:
        return redirect(url_for('bank.login'))

    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 0))
            if amount <= 0:
                flash("Deposit amount must be greater than zero.", "danger")
                return redirect(url_for('bank.deposit'))

            user.balance += amount
            user.credit_limit += amount / 10
            flash(f"${amount:.2f} deposited successfully!", "success")
            return redirect(url_for('bank.index'))
        except ValueError:
            flash("Invalid amount entered.", "danger")

    return render_template('deposit.html', account=user)


@bank_bp.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    user = get_current_user()
    if not user:
        return redirect(url_for('bank.login'))

    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 0))
            if amount <= 0:
                flash("Withdrawal amount must be greater than zero.", "danger")
                return redirect(url_for('bank.withdraw'))

            if amount > user.balance:
                flash("Insufficient balance for this withdrawal.", "danger")
                return redirect(url_for('bank.withdraw'))

            user.balance -= amount
            user.credit_limit = max(0.0, user.credit_limit - (amount / 10))
            flash(f"${amount:.2f} withdrawn successfully!", "success")
            return redirect(url_for('bank.index'))
        except ValueError:
            flash("Invalid amount entered.", "danger")

    return render_template('withdraw.html', account=user)


@bank_bp.route('/transfer', methods=['GET', 'POST'])
def transfer():
    user = get_current_user()
    if not user:
        return redirect(url_for('bank.login'))

    if request.method == 'POST':
        target_acc_num = request.form.get('target_account', '').strip()
        try:
            amount = float(request.form.get('amount', 0))

            if amount <= 0:
                flash("Transfer amount must be greater than zero.", "danger")
                return redirect(url_for('bank.transfer'))

            if amount > user.balance:
                flash("Insufficient funds for this transfer.", "danger")
                return redirect(url_for('bank.transfer'))

            if target_acc_num == user.account_number:
                flash("You cannot transfer money to your own account.", "warning")
                return redirect(url_for('bank.transfer'))

            recipient = get_account_by_number(target_acc_num)
            if not recipient:
                flash("Destination account number not found.", "danger")
                return redirect(url_for('bank.transfer'))

            user.balance -= amount
            recipient.balance += amount
            flash(f"${amount:.2f} successfully transferred to {recipient.name} (Acc: {recipient.account_number})!", "success")
            return redirect(url_for('bank.index'))

        except ValueError:
            flash("Invalid amount entered.", "danger")

    return render_template('transfer.html', account=user)


@bank_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for('bank.login'))