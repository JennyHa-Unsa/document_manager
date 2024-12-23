# create_db.py

import os
from app import create_app, db
from app.models import User, Role, Permission, RolePermission

# Crear una instancia de la aplicación
app = create_app()

# Usar el contexto de la aplicación para crear la base de datos
with app.app_context():
    # Eliminar la base de datos si existe
    db.drop_all()
    
    # Crear todas las tablas en la base de datos
    db.create_all()

    # Crear permisos si no existen
    permissions = ['read', 'write', 'delete', 'manage_users']
    permission_objects = {}
    for perm_name in permissions:
        perm = Permission.query.filter_by(name=perm_name).first()
        if not perm:
            perm = Permission(name=perm_name)
            db.session.add(perm)
        permission_objects[perm_name] = perm

    db.session.commit()

    # Crear roles si no existen
    roles = {
        'Lector': ['read'],
        'Editor': ['read', 'write'],
        # 'Administrador': ['read', 'write', 'delete', 'manage_users']
        'Administrador': ['read', 'write', 'manage_users']
    }
    role_objects = {}
    for role_name, perms in roles.items():
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.session.add(role)
        role_objects[role_name] = role
        db.session.commit()
        
        # Asociar permisos con el rol
        for perm_name in perms:
            permission = permission_objects[perm_name]
            role_permission = RolePermission.query.filter_by(role_id=role.id, permission_id=permission.id).first()
            if not role_permission:
                role_permission = RolePermission(role_id=role.id, permission_id=permission.id)
                db.session.add(role_permission)

    db.session.commit()

    # Crear usuarios si no existen
    users = [
        {'username': 'lector', 'email': 'lector@example.com', 'phone': '51962870787', 'password': 'lectorpass', 'role': role_objects['Lector']},
        {'username': 'editor', 'email': 'editor@example.com', 'phone': '51962870787', 'password': 'editorpass', 'role': role_objects['Editor']},
        {'username': 'admin', 'email': 'admin@example.com', 'phone': '51962870787', 'password': 'adminpass', 'role': role_objects['Administrador']}
    ]
    for user_data in users:
        user = User.query.filter_by(username=user_data['username']).first()
        if not user:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                phone=user_data['phone'],
                role=user_data['role']
            )
            user.set_password(user_data['password'])
            db.session.add(user)

    db.session.commit()

    print("Base de datos, roles, permisos y usuarios creados exitosamente.")
