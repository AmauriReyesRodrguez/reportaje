import os
from flask import Flask, redirect, render_template, url_for, flash, request
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from forms import Login, Registro
from models import User
from sqlalchemy import select
from extensions import db


app = Flask(__name__)

app.config['SECRET_KEY'] = 'clave_super_segura_123'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorial_flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


login_manager = LoginManager(app)
login_manager.login_view = 'ver_login'
login_manager.init_app(app)

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
    

@app.route("/")
@login_required
def index():
    return render_template('index.html', nombre=current_user.nombre)

@app.route("/registro/", methods=["GET", "POST"])
def ver_registro():
    # Si ya está logueado, redirigir al índice
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = Registro()

    if form.validate_on_submit():
     nombre = form.nombre.data
     email = form.email.data
     password = form.password.data  # Aquí deberías encriptar la contraseña

     nuevo_usuario = User(nombre=nombre, email=email, password=password)
     db.session.add(nuevo_usuario)
     db.session.commit()
     flash('Registro exitoso. Inicia sesión.', 'success')
     return redirect(url_for('ver_login'))

        

    # Si es un GET o un formulario inválido, solo mostrar el template
    return render_template("registro_form.html", objregistro=form)

@app.route("/login/", methods=["GET", "POST"])
def ver_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = Login()

    if form.validate_on_submit():
        user = db.session.execute(
            select(User).where(User.email == form.email.data)
        ).scalar_one_or_none()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Bienvenido de nuevo', 'success')
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas', 'danger')

    return render_template("login_form.html", objLogin=form)

@app.route("/chismes/")
def ver_chismes():
    return render_template('chismes.html')

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('ver_login'))


if __name__ == '__main__':
    
    from waitress import serve

    with app.app_context():
     db.create_all()  # ✅ crea todas las tablas del modelo
     
    port = int(os.environ.get("PORT", 8080))
    serve(app, host="0.0.0.0", port=port)