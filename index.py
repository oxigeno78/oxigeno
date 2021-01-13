from flask import Flask, render_template, redirect, url_for, request, session, abort, flash, make_response
import datetime
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "static/uploads/"

app.secret_key = "@daf12dda00#"

# Navegacion
@app.route('/')
def index():
    if 'username' in session:
        getUser = redirect(url_for('home'))
        return getUser
    else:
        return render_template('login.html', titulo="Identifícate!!!...")

@app.route('/favicon.ico')
def icono():
    return ''

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('index.html', titulo="Bienvenido!!!...", username=session['username'])
    else:
        getUserLogin = redirect(url_for('index'))
        return getUserLogin

@app.route('/about')
def about():
    if 'username' in session:
        return render_template('about.html', titulo="Nosotros...", username=session['username'])
    else:
        return redirect(url_for('index'))


@app.route('/upload')
def fileUpload():
    return render_template('uploadFile.html', titulo="Sube un archivo...", username=session['username'])

# API
# el método de solicitud (GET, POST, etc.) puede obtenerse por:
# request.method
# los argumentos enviados por URL pueden recuperarse con:
# reques.args.get("nombre del Argumento")

@app.route('/register', methods = ['POST'])
def register():
    usuario = request.form['username']
    mail = request.form['mail']
    passwd = request.form['password']
    logguer("[ "+ request.method + " "+ request.remote_addr  +" ] · request register: "+usuario+" "+ mail +" "+passwd)
    goToIndex = redirect(url_for('index'))
    return goToIndex

@app.route('/login', methods = ['POST'])
def login():
    usuario = request.form['usuario']
    passwd = request.form['password']
    if usuario == "" or passwd =="" :
        logguer("[ "+ request.method + " "+ request.remote_addr  +" ] · Intento de acceder con credenciales vacías desde ")
        abort(401)
    session['username'] = usuario
    logguer("[ "+ request.method + " "+ request.remote_addr  +" ] · request login: "+usuario+" "+passwd)
    flash("bienvenido!!!")
    goToHome = redirect(url_for('home'))
    return goToHome

@app.route('/logout')
def logout():
    logguer("[ "+ request.method + " "+ request.remote_addr  +" ] · request logout: "+session['username'])
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/uploader', methods = ['POST'])
def uploader():
    print(request.files)
    archivo = request.files['archivo']
    blob = request.files['archivo'].read()
    peso = len(blob)
    archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(archivo.filename)))
    flash("Exito!!!")
    goToUpload = redirect(url_for('fileUpload'))
    return goToUpload


# funciona para almacenar log's
def logguer(log):
    logLogin = open("login.txt","a")
    tiempo = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    logLogin.write(tiempo+" - "+ log+'\n')
    logLogin.close()


if __name__ == '__main__':
    app.run(debug=True)