# app/models/producto_model.py

from app._mysql_db import selectDB

class ProductoModel:

    @staticmethod
    def listar_todos(configDB):
        sql = "SELECT * FROM producto"
        return selectDB(configDB, sql)

    @staticmethod
    def buscar_por_categoria(configDB, categoria):
        sql = "SELECT * FROM producto WHERE categoria = %s"
        val = (categoria,)
        return selectDB(configDB, sql, val)

    @staticmethod
    def buscar_por_marca(configDB, marca):
        sql = "SELECT * FROM producto WHERE marca = %s"
        val = (marca,)
        return selectDB(configDB, sql, val)

    @staticmethod
    def obtener_por_id(configDB, id_producto):
        sql = "SELECT * FROM producto WHERE id = %s"
        val = (id_producto,)
        res = selectDB(configDB, sql, val)
        return res[0] if res else None