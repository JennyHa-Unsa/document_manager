# create_db.py

import os
from app import create_app, db
from app.models import User, Role

# Crear una instancia de la aplicación
app = create_app()

# Usar el contexto de la aplicación para crear la base de datos
with app.app_context():
    # Eliminar la base de datos si existe
    db.drop_all()
    
    # Crear todas las tablas en la base de datos
    db.create_all()

    # Crear roles si no existen
    lector_role = Role.query.filter_by(name='Lector').first()
    if not lector_role:
        lector_role = Role(name='Lector')
        db.session.add(lector_role)
    
    editor_role = Role.query.filter_by(name='Editor').first()
    if not editor_role:
        editor_role = Role(name='Editor')
        db.session.add(editor_role)
    
    admin_role = Role.query.filter_by(name='Administrador').first()
    if not admin_role:
        admin_role = Role(name='Administrador')
        db.session.add(admin_role)

    db.session.commit()

    # Crear usuarios si no existen
    lector = User.query.filter_by(username='lector').first()
    if not lector:
        lector = User(username='lector', email='lector@example.com', phone='51962870787', role=lector_role)
        lector.set_password('lectorpass')
        db.session.add(lector)

    editor = User.query.filter_by(username='editor').first()
    if not editor:
        editor = User(username='editor', email='editor@example.com', phone='51962870787', role=editor_role)
        editor.set_password('editorpass')
        db.session.add(editor)

    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com', phone='51962870787', role=admin_role)
        admin.set_password('adminpass')
        db.session.add(admin)

    db.session.commit()

    print("Base de datos, roles y usuarios creados exitosamente.")
