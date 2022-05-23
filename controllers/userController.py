import re
from string import punctuation
from flask import flash
from models.userModel import UserModel
from models.entitites.user_entity import User

def login(user: User):
    row = UserModel.getUserByEmail(user.email)
    if row != None:
        if row[5] == 'false':
            flash("Usuario sin confirmar","warning")
            return None
        else:
            user = UserModel.login(user)
            if user.password:
                return user
            else:
                flash("Contraseña invalida.","error")
                return None
    else:
        flash("Usuario no encontrado","error")
        return None

def getUserById(id):
    return UserModel.getUserById(id)

def getUserByEmail(email):
    return UserModel.getUserByEmail(email)

def crearUsuario(user: User):
    flash("Registro Exitoso, revisa tu correo y confirma tu cuenta","success")
    UserModel.crearUsuario(user)

def cambiarContraseña(password, token):
    UserModel.cambiarContraseña(password,token)

def emailUsed(email):
    return UserModel.emailUsed(email)

def emailValido(email):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, email) is not None

def generarToken(email):
    return UserModel.generarToken(email)

def validToken(token):
    return UserModel.validToken(token)

def confirmUser(token):
    UserModel.confirmUser(token)

def isValidForm(pagina, user: User):
    isValidUsername = True
    isValidEmail = True
    isValidPassword= True

    if pagina == 'registro':
        
        if user.username == "":
            isValidUsername = False
            flash("Nombre de usuario Obligatorio","warning")

        if user.email == "":
            isValidEmail = False
            flash("Email Obligatorio","warning")
        else:
            if not emailValido(user.email):
                isValidEmail = False
                flash("Ingresa un Email Valido","error")
            else:
                if emailUsed(user.email):
                    isValidEmail = False
                    flash("Email ya registrado","warning")
            
        isValidPassword = isValidFormPassword(user.password)
        
        return (isValidUsername and isValidEmail and isValidPassword)
    else:
        if pagina == 'login':
            if user.email == "":
                isValidEmail = False
                flash("El Email es Requerido","warning")

            if user.password == "":
                isValidPassword = False
                flash("La Contraseña es Requerida","warning")
        else:
            if pagina == "email-cambiar-contraseña":
                if user.email == "":
                    isValidEmail = False
                    flash("El Email es requerido","warning")
                else:
                    if not emailValido(user.email):
                        isValidEmail = False
                        flash("Ingresa un Email Valido","error")
                    else:
                        if not emailUsed(user.email):
                            isValidEmail = False
                            flash("El Email no se encuentra registrado","error")
            if pagina == "cambiar-contraseña":
                isValidPassword = isValidFormPassword(user.password)

        return (isValidUsername and isValidEmail and isValidPassword)


def isValidFormPassword(password: str):
    isValidPassword = True

    if password == "":
        isValidPassword = False
        flash("La Contraseña es Obligatoria","warning")
    else:
        if len(password) < 8:
            isValidPassword = False
            flash("La Contraseña debe tener minimo 8 caracteres","warning")

        if not any([caracter.isdigit() for caracter in password]):
            isValidPassword = False
            flash("La Contraseña debe tener: 1 numero.","warning")

        if not any([caracter.isupper() for caracter in password]):
            isValidPassword = False
            flash("La Contraseña debe tener: 1 una Mayuscula","warning")

        if not any([True if caracter in punctuation else False for caracter in password]):
            isValidPassword = False
            flash("La Contraseña debe tener: 1 caracter especial.","warning")
    
    return isValidPassword