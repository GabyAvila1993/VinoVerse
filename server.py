from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
import os

app = Flask(__name__, static_url_path='/static')

# Configuración de Flask y MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'vinoverse'
app.secret_key = 'supersecretkey'  # Asegúrate de usar una clave secreta segura en producción

mysql = MySQL(app)

# Configuración de Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Tienes que iniciar sesión para entrar a la página."

class User(UserMixin):
    def __init__(self, id, email, contraseña):
        self.id = id
        self.email = email
        self.contraseña = contraseña

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, email, contraseña FROM usuarios WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user[0], user[1], user[2])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT id, email, contraseña FROM usuarios WHERE email = %s", (email,))
            user = cur.fetchone()
        
        if user and user[2] == contraseña:  # Verifica que la contraseña sea correcta
            user_obj = User(user[0], user[1], user[2])
            login_user(user_obj)
            return redirect(url_for('index'))  # Redirige a la página de inicio
        else:
            flash('Credenciales inválidas', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('login'))

@app.route("/")
def index():
    return render_template("inicio.html")

if __name__ == '__main__':
    app.run(port=3000, debug=True)
