from dotenv import load_dotenv
import os

#Cargar el archivo .env a las variables de entorno
load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

MYSQL_HOSTNAME = os.environ.get('MYSQL_HOSTNAME')
MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
MYSQL_PORT = os.environ.get('MYSQL_PORT')

SMTP_HOSTNAME = os.environ.get('SMTP_HOSTNAME')
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')