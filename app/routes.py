from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import User
from app.forms import LoginForm, UploadForm
import os

# Crear un Blueprint para las rutas
bp = Blueprint('routes', __name__)

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
    files = os.listdir(os.path.join(os.getcwd(), 'uploads'))
    return render_template('index.html', files=files)

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.getcwd(), 'uploads', filename))
        flash('Archivo subido con éxito.', 'success')
        return redirect(url_for('routes.index'))
    return render_template('upload.html', form=form)

# Ruta para servir archivos desde el directorio uploads
@bp.route('/uploads/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'uploads'), filename)

@bp.route('/delete/<filename>', methods=['POST'])
@login_required
def delete(filename):
    file_path = os.path.join(os.getcwd(), 'uploads', filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('Archivo eliminado.', 'success')
    else:
        flash('Archivo no encontrado.', 'danger')
    return redirect(url_for('routes.index'))
