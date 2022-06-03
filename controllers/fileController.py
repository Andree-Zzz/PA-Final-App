from datetime import datetime
import os
from flask import flash
from models import fileModel

def isValidFormUpload(nombre, file,action='subir'):
    isValidNombre = True
    isValidFile = True
    if nombre == '':
        isValidNombre = False
        flash("El Nombre del Archivo es requerido")
    if action != 'editar':
        if not file:
            isValidFile = False
            flash("El Archivo es requerido")
    
    return (isValidNombre and isValidFile)

def guardarFile(nombre, file, userId, filenameEditar = ''):
    date = str(datetime.now().microsecond)+str(datetime.now().second)+str(datetime.now().hour)+str(datetime.now().day)+str(datetime.now().month)
    # Guardar el file del formulario
    if file:
        filename = date+file.filename
        pathFile = '/static/files/'+filename
        file.save('.'+pathFile)
        tipo = _getTypeFileByFilename(file.filename)
        iconFile = _setIconFile(filename)
        megas = (os.path.getsize('.'+pathFile))/1048576
        fileModel.guardarFile(filenameEditar,nombre, filename, pathFile, tipo, megas, iconFile, userId)
    else:
        fileModel.guardarFile(filenameEditar,nombre)
        

def getFilesByUderId(userId):
    return fileModel.getFilesByUderId(userId)

def getFileByFilename(filename: str):
    return fileModel.getFileByFilename(filename)

def deleteFile(filename: str):
    fileModel.deleteFile(filename)

def _getTypeFileByFilename(filename: str):
    tipo = filename.split('.')
    return tipo[tipo.__len__()-1]

def _setIconFile(filename: str):
    tipo = _getTypeFileByFilename(filename)
    iconFile = '/static/icons-files/generico.png'
    if tipo == 'txt':
        iconFile = '/static/icons-files/txt.png'
    if tipo == 'docx' or tipo == 'doc':
        iconFile = '/static/icons-files/word.png'
    if tipo == 'xlsx' or tipo == 'xls':
        iconFile = '/static/icons-files/excel.png'
    if tipo == 'pdf':
        iconFile = '/static/icons-files/pdf.png'
    if tipo == 'pptx' or tipo == 'ppt':
        iconFile = '/static/icons-files/powerpoint.png'
    if tipo == 'csv':
        iconFile = '/static/icons-files/csv.png'
    if tipo == 'jpg' or tipo == 'jpeg' or tipo == 'png' or tipo == 'gif' or tipo == 'tiff' or tipo == 'svg':
        iconFile = '/static/files/'+filename

    return iconFile