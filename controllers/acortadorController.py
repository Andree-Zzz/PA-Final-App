from random import choice
import string
from flask import request
from models import acortadorModel

acortadorModel = acortadorModel.acortadorModel

def getLastFiveUrlsShort():
    return acortadorModel.getLastFiveUrlsShort()

def generate_short_id(num_of_chars: int):
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))

def createUrlShort(url: str):
    url_short = request.host_url+generate_short_id(4)
    acortadorModel.createUrlShort(url,url_short)

def getUrlByUrlShort(url_short: str):
    return acortadorModel.getUrlByUrlShort(url_short)