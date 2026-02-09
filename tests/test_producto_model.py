import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.config_db import POWERLAB_DB
from app.models.producto_model import ProductoModel

def main():
    todos = ProductoModel.listar_todos(POWERLAB_DB)
    print("TODOS:", len(todos))

    creatina = ProductoModel.buscar_por_categoria(POWERLAB_DB, "creatina")
    print("CREATINA:", len(creatina))

    ena = ProductoModel.buscar_por_marca(POWERLAB_DB, "Ena")
    print("ENA:", len(ena))

    p1 = ProductoModel.obtener_por_id(POWERLAB_DB, 1)
    print("ID 1:", p1[1] if p1 else None)

if __name__ == "__main__":
    main()