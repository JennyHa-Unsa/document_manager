from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class UploadForm(FlaskForm):
    file = FileField('Archivo', validators=[DataRequired()])
    is_public = BooleanField('¿Hacer público?', default=False)  # Campo añadido para marcar si el archivo será público
    submit = SubmitField('Subir')
