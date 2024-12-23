from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.forms import LoginForm, UploadForm
from app.models import User, Document, Role, Permission, DocumentAccess
import os

# Crear un Blueprint para las rutas
bp = Blueprint('routes', __name__)

# Función para verificar si el usuario tiene el permiso adecuado
def has_permission(permission_name):
    return any(permission.name == permission_name for permission in current_user.role.permissions)

@bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    return redirect(url_for('routes.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('routes.index'))
        flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente.', 'success')
    return redirect(url_for('routes.login'))

@bp.route('/index')
@login_required
def index():
    # Filtrar documentos públicos y mostrarlos solo a los usuarios que tienen acceso
    files = []
    if has_permission('leer'):
        # Si el usuario tiene el permiso de leer, mostrar documentos públicos
        documents = Document.query.filter_by(is_public=True).all()
        files = [doc.filename for doc in documents]
    return render_template('index.html', files=files)

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if not has_permission('subir'):
        flash('No tienes permiso para subir documentos.', 'danger')
        return redirect(url_for('routes.index'))
    
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(os.getcwd(), 'uploads', filename)
        file.save(file_path)

        # Guardar el documento en la base de datos
        document = Document(filename=filename, path=file_path, owner_id=current_user.id, is_public=False)
        db.session.add(document)
        db.session.commit()

        flash('Archivo subido con éxito.', 'success')
        return redirect(url_for('routes.index'))
    
    return render_template('upload.html', form=form)

@bp.route('/uploads/<filename>')
@login_required
def download_file(filename):
    # Verificar si el usuario tiene permiso para descargar el archivo
    document = Document.query.filter_by(filename=filename).first()
    if not document:
        flash('Documento no encontrado.', 'danger')
        return redirect(url_for('routes.index'))

    # Verificar si el usuario tiene acceso al archivo
    if not has_permission('descargar') or (document.owner_id != current_user.id and not has_permission('administrar')):
        flash('No tienes permiso para descargar este documento.', 'danger')
        return redirect(url_for('routes.index'))

    return send_from_directory(os.path.join(os.getcwd(), 'uploads'), filename)

@bp.route('/delete/<filename>', methods=['POST'])
@login_required
def delete(filename):
    # Buscar el documento por nombre
    document = Document.query.filter_by(filename=filename).first()
    if not document:
        flash('Documento no encontrado.', 'danger')
        return redirect(url_for('routes.index'))

    # Verificar permisos de eliminación
    if current_user.id == document.owner_id or has_permission('administrar'):
        # Eliminar el archivo de la base de datos y del sistema de archivos
        os.remove(document.path)
        db.session.delete(document)
        db.session.commit()
        flash('Documento eliminado con éxito.', 'success')
    else:
        flash('No tienes permiso para eliminar este documento.', 'danger')

    return redirect(url_for('routes.index'))
