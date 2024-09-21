from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
import os, MySQLdb.cursors



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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        contraseña = request.form['contraseña']
        confirm_password = request.form['confirm_password']
        
        if contraseña != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('register'))
        
        with mysql.connection.cursor() as cur:
            # Verificar si el correo ya está registrado
            cur.execute("SELECT email FROM usuarios WHERE email = %s", (email,))
            existing_user = cur.fetchone()
            
            if existing_user:
                flash('El correo ya está registrado', 'error')
                return redirect(url_for('register'))
            
            # Guardar el usuario en la base de datos sin hash
            cur.execute("INSERT INTO usuarios (nombre, apellido, email, contraseña, fecha_registro) VALUES (%s, %s, %s, %s, NOW())",
                        (nombre, apellido, email, contraseña))
            mysql.connection.commit()
        
        flash('Registro exitoso, ahora puedes iniciar sesión', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('login'))

@app.route("/inicio")
def index():
    return render_template("inicio.html")

@app.route("/")
def presetntacion():
    return render_template("principal.html")



#-------------------------------------------------------------------------------------------------------------------------
#                                           Obtencion de datos de perfil
#-------------------------------------------------------------------------------------------------------------------------

@app.route('/perfil/<int:usuario_id>')
def perfil(usuario_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Verificamos perfil del usuario
    cur.execute('SELECT * FROM perfiles WHERE usuario_id = %s', [usuario_id])
    perfil = cur.fetchone()
    
    if not perfil:
        flash('Perfil no encontrado')
        return redirect(url_for('register'))
    
    # Verificamos que el usuario este registrado
    cur.execute('SELECT * FROM usuarios WHERE id = %s', [usuario_id])
    usuario = cur.fetchone()
    
    if not usuario:
        flash('Usuario no encontrado')
        return redirect(url_for('register'))

    # Colocamos el nombre y el apellido con la primer letra en mayuscula
    usuario['nombre'] = usuario['nombre'].capitalize()
    usuario['apellido'] = usuario['apellido'].capitalize()

    # Buscamos las publicaciones del usuario
    cur.execute('SELECT * FROM publicaciones WHERE usuario_id = %s', [usuario_id])
    publicaciones = cur.fetchall()  # Obtener todas las publicaciones

    # Si no hay publicaciones, pasar una lista vacía al template
    if not publicaciones:
        publicaciones = []
        flash('No hay publicaciones recientes', 'info')

    # Pasar los datos del usuario y las publicaciones al template
    return render_template('perfil_layout.html', usuario=usuario, perfil=perfil, publicaciones=publicaciones)


#--------------------------------------------------------------------------------------------------------------------
#                                      Agregar publicacion a la tabla publicaciones
#--------------------------------------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------------------------
#                                      Agregar publicacion a la tabla publicaciones
#--------------------------------------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------------------------
#                                      Agregar publicacion a la tabla publicaciones
#--------------------------------------------------------------------------------------------------------------------






#--------------------------------
#     DEJAR ESTO AL FINAL
if __name__ == '__main__':
    app.run(port=3000, debug=True)
