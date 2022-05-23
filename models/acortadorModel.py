from config.database import db

class acortadorModel:

    def getLastFiveUrlsShort():
        cursor = db.cursor()
        cursor.execute("SELECT * FROM acortador ORDER BY id DESC LIMIT 5")
        urlItems = cursor.fetchall()
        cursor.close()
        return urlItems
    
    def createUrlShort(url: str, url_short: str):
        cursor = db.cursor()
        cursor.execute("INSERT INTO acortador(url,url_short) VALUES(%s,%s)",(
            url,
            url_short,
        ))
        cursor.close()
    
    def getUrlByUrlShort(url_short: str):
        cursor = db.cursor()
        cursor.execute("SELECT url FROM acortador WHERE url_short = %s LIMIT 1", (url_short,))
        url = cursor.fetchone()
        cursor.close()
        return url