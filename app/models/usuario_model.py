# app/models/usuario_model.py

from app._mysql_db import selectDB, insertDB

class UsuarioModel:

    @staticmethod
    def login(configDB, email, password):
        sql = "SELECT * FROM usuario WHERE email = %s AND pass = %s"
        val = (email, password)
        res = selectDB(configDB, sql, val)
        return res[0] if res else None

    @staticmethod
    def obtener_por_id(configDB, id_usuario):
        sql = "SELECT * FROM usuario WHERE id = %s"
        val = (id_usuario,)
        res = selectDB(configDB, sql, val)
        return res[0] if res else None

    @staticmethod
    def crear_usuario(configDB, nombre, apellido, email, telefono, direccion, password, tipo_usuario="usuario"):
        sql = """
            INSERT INTO usuario(id, nombre, apellido, email, telefono, direccion, pass, tipo_usuario)
            VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)
        """
        val = (nombre, apellido, email, telefono, direccion, password, tipo_usuario)
        return insertDB(configDB, sql, val)