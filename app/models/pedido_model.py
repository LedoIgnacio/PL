# app/models/pedido_model.py

from app._mysql_db import selectDB, insertDB, updateDB

class PedidoModel:

    @staticmethod
    def obtener_carrito_activo(configDB, id_usuario):
        sql = """
            SELECT * FROM pedido
            WHERE id_usuario = %s AND estado = 'carrito'
            ORDER BY id DESC
            LIMIT 1
        """
        val = (id_usuario,)
        res = selectDB(configDB, sql, val)
        return res[0] if res else None

    @staticmethod
    def crear_carrito(configDB, id_usuario):
        sql = "INSERT INTO pedido(id, id_usuario, fecha_hora, estado, total) VALUES (NULL, %s, NOW(), 'carrito', 0)"
        val = (id_usuario,)
        return insertDB(configDB, sql, val)

    @staticmethod
    def actualizar_total(configDB, id_pedido, total):
        sql = "UPDATE pedido SET total = %s WHERE id = %s"
        val = (total, id_pedido)
        return updateDB(configDB, sql, val)
    
    @staticmethod
    def cerrar_carrito_en_proceso(configDB, id_pedido):
        sql = """
            UPDATE pedido
            SET estado = 'en_proceso'
            WHERE id = %s AND estado = 'carrito'
        """
        val = (id_pedido,)
        return updateDB(configDB, sql, val)

    @staticmethod
    def listar_por_usuario(configDB, id_usuario):
        sql = """
            SELECT * FROM pedido
            WHERE id_usuario = %s AND estado <> 'carrito'
            ORDER BY fecha_hora DESC
        """
        val = (id_usuario,)
        return selectDB(configDB, sql, val)

    @staticmethod
    def obtener_por_id(configDB, id_pedido):
        sql = "SELECT * FROM pedido WHERE id = %s"
        val = (id_pedido,)
        res = selectDB(configDB, sql, val)
        return res[0] if res else None
    
    @staticmethod
    def listar_todos(configDB):
        sql = "SELECT * FROM pedido ORDER BY fecha_hora DESC"
        return selectDB(configDB, sql)

    @staticmethod
    def listar_por_estado(configDB, estado):
        sql = "SELECT * FROM pedido WHERE estado = %s ORDER BY fecha_hora DESC"
        val = (estado,)
        return selectDB(configDB, sql, val)

    @staticmethod
    def cambiar_estado(configDB, id_pedido, nuevo_estado):
        sql = "UPDATE pedido SET estado = %s WHERE id = %s"
        val = (nuevo_estado, id_pedido)
        return updateDB(configDB, sql, val)