#!/usr/bin/python3
import os
import sys

# 1. Importazione mancante
from wsgiref.handlers import CGIHandler

# 2. Configurazione percorsi
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(path, 'libs'))
sys.path.insert(0, path)

# 3. Importazione della tua app Flask
try:
    from app import app
except ImportError as e:
    print("Content-Type: text/html\n")
    print(f"<h1>Errore di Importazione</h1><p>{e}</p>")
    sys.exit()

# 4. ProxyFix per gestire correttamente le richieste HTTP tramite CGI
class ProxyFix(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        # Corregge i dati dell'ambiente che CGI spesso passa in modo errato
        environ['SERVER_NAME'] = os.environ.get('SERVER_NAME', 'localhost')
        environ['SERVER_PORT'] = os.environ.get('SERVER_PORT', '80')
        environ['REQUEST_METHOD'] = os.environ.get('REQUEST_METHOD', 'GET')
        environ['SCRIPT_NAME'] = ""
        # Gestisce il path per evitare l'errore 404 sulle rotte Flask
        PATH_INFO = environ.get('PATH_INFO', '')
        if not PATH_INFO and 'REQUEST_URI' in environ:
            PATH_INFO = environ['REQUEST_URI'].split('?')[0]
        environ['PATH_INFO'] = PATH_INFO
        
        return self.app(environ, start_response)

app.wsgi_app = ProxyFix(app.wsgi_app)

# 5. Esecuzione
if __name__ == '__main__':
    CGIHandler().run(app)