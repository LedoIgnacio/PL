import os
import sys

# agrega la carpeta raíz del proyecto al path (PL/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
    
from app.config_db import POWERLAB_DB
from app._mysql_db import selectDB

def main():
    sql = "SELECT * FROM producto"
    res = selectDB(POWERLAB_DB, sql)

    if res is None:
        print("ERROR: selectDB devolvió None (falló conexión o query).")
        return

    print("OK - filas:", len(res))
    for fila in res[:3]:
        print(fila)

if __name__ == "__main__":
    main()