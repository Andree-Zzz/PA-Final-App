import logging
from flask import current_app
from smtplib import SMTP, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread
from flask import render_template

from config import settings

def emailBienvenida(username, email, url):
    send_email(
        asunto='Bienvenido, Registro Exitoso',
        destinatario=email,
        msg_html=render_template("sistema-archivos/mails/bienvenidaMail.html", username = username, url = url)
    )

def emailCambiarPassword(username, email, url):
    send_email(
        asunto='Cambiar mi contraseña',
        destinatario=email,
        msg_html=render_template("sistema-archivos/mails/cambiarContraseñaMail.html", username = username, url = url)
    )

def send_email(asunto, destinatario, msg_html):
    message = MIMEMultipart()
    
    message['Subject'] = asunto
    message['From'] = settings.SMTP_USERNAME
    message['To'] = destinatario
    msg_html = MIMEText(msg_html, 'html')
    message.attach(msg_html)
    Thread(
        target=_send_async_email,
        args=(current_app._get_current_object(), message)
    ).start()

logger = logging.getLogger(__name__)

def _send_async_email(app, message):
    with app.app_context():
        try:
            username = settings.SMTP_USERNAME
            password = settings.SMTP_PASSWORD

            server = SMTP(settings.SMTP_HOSTNAME)
            server.starttls()
            server.login(username,password)
            server.sendmail(username, message['To'], message.as_string())
            del message['Subject']
            del message['From']
            del message['To']
            server.quit()
        except SMTPException:
            logger.exception("Ocurrió un error al enviar el email")