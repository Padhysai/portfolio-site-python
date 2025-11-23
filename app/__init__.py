import os
from flask import Flask
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from .services import database, auth_manager, mongo

# Load environment variables
load_dotenv()

from .utils import get_client_ip

# Initialize Extensions
talisman = Talisman()
limiter = Limiter(key_func=get_client_ip, storage_uri="memory://")
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Config
    app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
    app.config['ADMIN_USERNAME'] = os.getenv('ADMIN_USERNAME', 'admin')
    app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD', 'password123')
    app.config['ADMIN_EMAIL'] = os.getenv('ADMIN_EMAIL', 'your-email@gmail.com')
    
    # Initialize Extensions with App
    csp = {
        'default-src': '\'self\'',
        'script-src': [
            '\'self\'',
            '\'unsafe-inline\'',
            'https://unpkg.com',
            'https://cdn.jsdelivr.net',
            'https://fonts.googleapis.com'
        ],
        'style-src': [
            '\'self\'',
            '\'unsafe-inline\'',
            'https://fonts.googleapis.com',
            'https://cdn.jsdelivr.net',
            'https://maxcdn.bootstrapcdn.com'
        ],
        'font-src': [
            '\'self\'',
            'https://fonts.gstatic.com',
            'https://cdn.jsdelivr.net',
            'https://maxcdn.bootstrapcdn.com'
        ],
        'img-src': ['\'self\'', 'data:', 'https:'],
        'object-src': '\'none\''
    }
    talisman.init_app(app, content_security_policy=csp, force_https=False)
    limiter.init_app(app)
    csrf.init_app(app)
    
    # Initialize DB
    mongo.init_mongo(app)
    database.init_db()
    
    # Initialize OAuth
    auth_manager.init_oauth(app)
    
    # Register Blueprints
    from .routes.main import main_bp
    from .routes.admin import admin_bp
    from .routes.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    
    return app
