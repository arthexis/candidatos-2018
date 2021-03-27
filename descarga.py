from urllib.parse import urljoin
from json import loads

from httpx import get
import sqlite3
from sqlite_utils import Database


base_url = "https://candidaturas.ine.mx/documentos/json/" 

# Aqui se pone cada una de las tablas que queramos crear:
# nombre_tabla: (archivo_json, llave_json)
# La llave es la que contiene la lista de candidatos
resources = {
    'diputados_federales': ('diputadosFederalesMR.json', 'candidatos')
}

# La DB que se va a crear, si ya existe hay que borrarla manualmente primero
db = Database(sqlite3.connect("ine-2018.db"))

for table, (url, key) in resources.items():
    decoded = get(urljoin(base_url, url)).content.decode('utf-8')
    # Hacemos esto porque el json no viene limpio, tiene algo de texto antes
    rows = loads(decoded.split("=", 1)[1])[key]
    print(f'Se descargaron {len(rows)} {table}')
    db[table].insert_all(rows)
