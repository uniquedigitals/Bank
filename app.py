import os
from flask import Flask
from routes import bank_bp

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'super_secret_bank_key')

app.register_blueprint(bank_bp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)