# create_db.py

from app import create_app, db
from app.models import User

# Crear una instancia de la aplicación
app = create_app()

# Usar el contexto de la aplicación para crear la base de datos
with app.app_context():
    # Crear todas las tablas en la base de datos
    db.create_all()
    
    # Crear un usuario admin si no existe
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin')
        admin.set_password('adminpass')
        db.session.add(admin)
        db.session.commit()

    print("Base de datos y usuario admin creados exitosamente.")
