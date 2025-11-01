from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class Registro(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=67)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    repetir_password = PasswordField('Repetir Contraseña', validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')])
    enviar = SubmitField('Registrar')
   

class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    enviar = SubmitField('Iniciar Sesión')