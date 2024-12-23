from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Inicialización de extensiones
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    
    # Cargar configuraciones desde config.py
    app.config.from_object(Config)

    # Inicializar extensiones con la aplicación
    db.init_app(app)
    login_manager.init_app(app)

    # Registrar la función user_loader
    # Importar dentro de la función para evitar la importación circular
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Importar y registrar blueprints o rutas
    from app import routes
    app.register_blueprint(routes.bp)

    return app
