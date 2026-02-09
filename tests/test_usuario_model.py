import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.config_db import POWERLAB_DB
from app.models.usuario_model import UsuarioModel

def main():
    # usa un usuario que exista en tu SQL
    user = UsuarioModel.login(POWERLAB_DB, "ignacioledo@uca.edu.ar", "1234")

    if not user:
        print("LOGIN: FAIL")
        return

    print("LOGIN: OK")
    # usuario: (id, nombre, apellido, email, telefono, direccion, pass, tipo_usuario)
    print("ID:", user[0])
    print("NOMBRE:", user[1], user[2])
    print("EMAIL:", user[3])
    print("TIPO:", user[7])

if __name__ == "__main__":
    main()