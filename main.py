import os
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect

from models.entitites.user_entity import User
from config.settings import SECRET_KEY
from send_email import emailCambiarPassword

from controllers import fileController, userController, acortadorController, ocr_controller


app = Flask(__name__)

app.secret_key = SECRET_KEY
csrf = CSRFProtect(app)
login_manager_app = LoginManager(app)

# *Sistema de archivos

@login_manager_app.user_loader
def load_user(id):
    return userController.getUserById(id)

@app.get("/")
def index():
    if not current_user:
        return redirect(url_for("login"))
    else:
        return redirect(url_for("misArchivos"))

@app.get("/registro")
def registro():
    return render_template("final-app/auth/registro_login.html", pagina = 'Registro')

@app.post("/registro")
def registrarUsuario():
    user = User(0,request.form.get('username'),request.form.get('email'),request.form.get('password'),None,None)
    isValid = userController.isValidForm('registro',user)
    if isValid == False:
        return render_template(
            "final-app/auth/registro_login.html",
            pagina = 'Registro',
            username = user.username,
            email = user.email
        )
    else:
        userController.crearUsuario(user)
        return render_template(
            "final-app/auth/registro_login.html",
            pagina = 'Registro'
        )

@app.get("/login")
def login():
    return render_template("final-app/auth/registro_login.html", pagina = 'Iniciar sesion')

@app.post("/login")
def loginPost():
    user = User(0,None,request.form.get('email'),request.form.get('password'),None,None)
    
    isValid = userController.isValidForm('login',user)
    if isValid == False:
        return render_template(
            "final-app/auth/registro_login.html",
            pagina = 'Iniciar sesion',
            username = user.username,
            email = user.email
        )
    else:
        user_logeado = userController.login(user)
        if user_logeado != None:
            login_user(user_logeado)
            return redirect(url_for('misArchivos'))
        else:
            return render_template("final-app/auth/registro_login.html", pagina = 'Iniciar sesion', email = user.email)

@app.get("/cambiar-contraseña")
def cambiarPassword():
    return render_template('final-app/auth/emailCambiarPassword.html')

@app.post("/cambiar-contraseña")
def cambiarPasswordPost():
    user = User(0,'',request.form.get('email'),None,None,None)
    isValid = userController.isValidForm('email-cambiar-contraseña',user)
    if isValid == False:
        return render_template("final-app/auth/emailCambiarPassword.html")
    else:
        row = userController.getUserByEmail(user.email)
        user.id = row[0]
        user.username = row[1]
        token = userController.generarToken(user.email)
        url = request.host_url+"cambiar-contraseña/"+token
        emailCambiarPassword(user.username, user.email, url)
        flash("Email de cambio de contraseña enviado","success")
        return redirect(url_for('login'))

@app.get("/cambiar-contraseña/<token>")
def cambiarPasswordToken(token):
    validToken = userController.validToken(token)
    if validToken != None:
        return render_template('final-app/auth/cambiarPassword.html',token=token)
    else:
        flash("Contraseña cambiada","success")
        return redirect(url_for('login'))

@app.post("/cambiar-contraseña/cambiar")
def cambiarPasswordTokenPost():
    token = request.form.get("token")
    isValidToken = userController.validToken(token)
    if isValidToken != None:
        password = request.form.get("password")
        user = User(0,None,None,password,None,None)
        isValidForm = userController.isValidForm("cambiar-contraseña",user)
        if isValidForm == False:
            return render_template("final-app/auth/cambiarPassword.html")
        else:
            userController.cambiarContraseña(password,token)
            return redirect(url_for('login'))
    else:
        return "Token perdido o invalido"

@app.get("/confirm/<token>")
def confirm(token):
    token = userController.validToken(token)
    if id!= None:
        userController.confirmUser(token)
        return render_template('final-app/auth/confirm.html')
    else:
        return "Token invalido: "+token

@app.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.get("/mis-archivos")
@login_required
def misArchivos():
    userId = current_user.id
    files = fileController.getFilesByUderId(userId)
    return render_template("final-app/home/misArchivos.html", files=files)

@app.get("/subir-archivos")
@login_required
def subirArchivos():
    return render_template("final-app/home/subirArchivos.html",action='subir')

@app.post("/subir-archivos")
@login_required
def subirArchivosPost():
    userId = current_user.id
    nombre = request.form.get("nombreArchivo")
    file = request.files['file']
    isValidForm= fileController.isValidFormUpload(nombre,file)
    if isValidForm == False:
        return render_template("final-app/home/subirArchivos.html", nombre=nombre,action='subir')
    fileController.guardarFile(nombre,file,userId)
    return redirect(url_for("misArchivos"))

@app.get("/editar-archivo/<nombre>/<filename>")
@login_required
def editarArchivo(nombre,filename):
    return render_template("final-app/home/subirArchivos.html",nombre=nombre,filename=filename,action='editar')

@app.post("/editar-archivo/<nombre>/<filename>")
@login_required
def editarArchivoPost(nombre,filename):

    userId = current_user.id
    nombreform = request.form.get("nombreArchivo")
    file = request.files['file']

    isValidForm= fileController.isValidFormUpload(nombreform,file,'editar')
    if isValidForm == False:
        return render_template("final-app/home/subirArchivos.html", nombre=nombreform,filename=filename,action='editar')

    if nombre == nombreform and not file:
        return redirect(url_for('misArchivos'))

    if file:
        os.remove("./static/files/"+filename)
    
    fileController.guardarFile(nombreform,file,userId,filenameEditar=filename)

    return redirect(url_for("misArchivos"))

@app.get("/detalles-archivo/<filename>")
def detallesArchivo(filename):
    file = fileController.getFileByFilename(filename)
    url = request.host_url+'detalles-archivo/'+file[2]
    return render_template("final-app/home/detallesArchivo.html",file=file,url=url)

@app.get("/eliminar-archivo/<filename>")
@login_required
def eliminarArchivo(filename):
    fileController.deleteFile(filename)
    os.remove("./static/files/"+filename)
    return redirect(url_for("misArchivos"))


# *Acortador de enlaces

@app.get("/acortador")
def acortador():
    lastFiveUrlShort = acortadorController.getLastFiveUrlsShort()
    return render_template("final-app/home/acortador.html",lastFiveUrlShort = lastFiveUrlShort)

@app.post("/")
def crearShort():
    url = request.form.get('url')
    if url:
        acortadorController.createUrlShort(url)
    return redirect(url_for("index"))

@app.get("/<url_short>")
def redirect_url_short(url_short):
    url_short = request.host_url+url_short
    url = acortadorController.getUrlByUrlShort(url_short)
    if(url != None):
        return redirect(url[0])
    else:
        return redirect(url_for('index'))


# *Obtener el texto dentro de una imagen

@app.get("/get-text-from-image")
def getTextFromImage():
    return render_template("final-app/home/form_text_image.html")

@app.post("/get-text-from-image")
def procesar_imagen():
    ocr_controller.deleteFiles()
    # Obtener la imagen del formulario
    imagen = request.files['imagen']
    # Evaluar si envio una imagen o no dentro del formulario
    if imagen:
        # Guardar la imagen y obtener su ruta de ubicacion
        pathImage = ocr_controller.saveImage(imagen)
        # Procesar la imagen y obtener su texto 
        # recibiendo su ruta de ubicacion (por ahora Funciona con texto en Ingles)
        text_image = ocr_controller.getTextImage(pathImage)
        return render_template('final-app/home/resp_text_image.html', text_image = text_image, pathImage = pathImage)
    else:
        # TODO: Feedback seleccionar imagen
        return redirect(url_for('getTextFromImage'))


# No autorizado
def status_401(error):
    return redirect(url_for('login'))

# Pagina no encontrada
def status_404(error):
    
    return "<h1>404: Pagina no encontrada...<h1/>"

app.register_error_handler(401,status_401)
app.register_error_handler(404,status_404)
csrf.init_app(app)

# app.run(debug=True)# Comentar para desplieges a Heroku

if __name__ == '__main__':
    index()