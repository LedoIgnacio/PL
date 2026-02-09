# app/models/pedido_detalle_model.py

from app._mysql_db import selectDB, insertDB, updateDB, deleteDB

class PedidoDetalleModel:

    @staticmethod
    def agregar_item(configDB, id_pedido, id_producto, cantidad, precio_uni):
        sql = """
            INSERT INTO pedido_detalle(id, id_pedido, id_producto, cantidad, precio_uni)
            VALUES (NULL, %s, %s, %s, %s)
        """
        val = (id_pedido, id_producto, cantidad, precio_uni)
        return insertDB(configDB, sql, val)

    @staticmethod
    def listar_por_pedido(configDB, id_pedido):
        sql = """
            SELECT pd.id, pd.id_pedido, pd.id_producto, pd.cantidad, pd.precio_uni,
                   p.nombre, p.marca
            FROM pedido_detalle pd
            JOIN producto p ON p.id = pd.id_producto
            WHERE pd.id_pedido = %s
        """
        val = (id_pedido,)
        return selectDB(configDB, sql, val)

    @staticmethod
    def calcular_total_pedido(configDB, id_pedido):
        sql = "SELECT IFNULL(SUM(cantidad * precio_uni), 0) FROM pedido_detalle WHERE id_pedido = %s"
        val = (id_pedido,)
        res = selectDB(configDB, sql, val)
        # res[0] es una tupla de 1 elemento: (total,)
        return res[0][0] if res else 0
    
    @staticmethod
    def actualizar_cantidad(configDB, id_pedido, id_producto, cantidad):
        sql = """
            UPDATE pedido_detalle
            SET cantidad = %s
            WHERE id_pedido = %s AND id_producto = %s
        """
        val = (cantidad, id_pedido, id_producto)
        return updateDB(configDB, sql, val)

    @staticmethod
    def eliminar_item(configDB, id_pedido, id_producto):
        sql = "DELETE FROM pedido_detalle WHERE id_pedido = %s AND id_producto = %s"
        val = (id_pedido, id_producto)
        return deleteDB(configDB, sql, val)

    @staticmethod
    def vaciar_pedido(configDB, id_pedido):
        sql = "DELETE FROM pedido_detalle WHERE id_pedido = %s"
        val = (id_pedido,)
        return deleteDB(configDB, sql, val)