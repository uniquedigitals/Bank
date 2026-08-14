import os
from flask import Flask
from routes import bank_bp

app = Flask(__name__)
# Uses Railway's secret key variable in production, falls back to default locally
app.secret_key = os.environ.get('SECRET_KEY', 'super_secret_bank_key_change_in_production')

# Register all routes defined in routes.py
app.register_blueprint(bank_bp)

if __name__ == '__main__':
    # Dynamically bind to Railway's assigned PORT (defaults to 5001 locally)
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)