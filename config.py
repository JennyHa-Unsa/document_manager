# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    # Verificar si la carpeta de uploads existe, si no, crearla
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)