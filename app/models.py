from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Tabla para los usuarios
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(150), nullable=False)
    
    # Relación con el rol
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', back_populates='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.id)  # Retorna la ID del usuario como una cadena

# Tabla para los roles
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relación inversa con los usuarios
    users = db.relationship('User', back_populates='role')

    # Relación con permisos
    permissions = db.relationship('Permission', secondary='role_permission', back_populates='roles')

# Tabla para los permisos
class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Relación con los roles
    roles = db.relationship('Role', secondary='role_permission', back_populates='permissions')

# Tabla intermedia para la relación muchos a muchos entre roles y permisos
class RolePermission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))

# Tabla para los documentos
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    path = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    is_public = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relación con el propietario (usuario que subió el archivo)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref='documents', lazy=True)

    # Relación con los accesos a documentos
    access_rights = db.relationship('DocumentAccess', back_populates='document')

# Tabla para los accesos de documentos (quién puede hacer qué con un documento)
class DocumentAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))

    # Relaciones
    user = db.relationship('User', backref='document_access', lazy=True)
    document = db.relationship('Document', back_populates='access_rights')
    permission = db.relationship('Permission')

