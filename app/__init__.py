from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Inicialización de extensiones
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'

def create_app():
    app = Flask(__name__)
    
    # Cargar configuraciones desde config.py
    app.config.from_object(Config)

    # Inicializar extensiones con la aplicación
    db.init_app(app)
    login_manager.init_app(app)

    # Importar y registrar blueprints o rutas
    from app import routes
    app.register_blueprint(routes.bp)

    return app
