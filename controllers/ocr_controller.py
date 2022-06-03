from datetime import datetime
import os

from PIL import Image
import pytesseract

from config.settings import PATH_TESSERACT_CMD

# Guardar la imagen del formulario y asi poder hacer el proceso de
# deteccion del texto.
def saveImage(image):
    code_date = str(datetime.now().day)+str(datetime.now().month)+str(datetime.now().hour)+str(datetime.now().second)+str(datetime.now().microsecond)
    pathfile = '/static/images/'+code_date+image.filename
    image.save(f'.{pathfile}')
    return pathfile

# Eliminar todos las imagenes almacenadas
def deleteFiles():
    for x in os.listdir('static/images'):
        # No borrar el archivo .gitignore
        if x != '.gitignore':
            os.remove(os.path.join('static/images', x))
    return None

# Obtener el texto de la imagen
# pidiendo como parametro su ubicacion de guardado
def getTextImage(pathImage) -> str:
    img = Image.open(f'.{pathImage}')
    # Acceso a la biblioteca ejecutable de tesseract ocr
    # La cual tiene las funciones de reconocimiento
    pytesseract.pytesseract.tesseract_cmd = PATH_TESSERACT_CMD
    # Procesar la imagen para obeneter el texto
    # con la funcion que dispone pytesseract
    text_image = pytesseract.image_to_string(img).strip()
    # text_image = pytesseract.image_to_string(img, lang='spa').strip()

    if len(text_image) == 0:
        return '*'
    else:
        return text_image
    # print(f'txtImg:{text_image}#')