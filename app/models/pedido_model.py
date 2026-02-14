from app._mysql_db import selectDB, insertDB, updateDB

class PedidoModel:

    @staticmethod
    def listar_pedidos_por_usuario(configDB, user_id):
        sql = """
            SELECT id, id_usuario, fecha_hora, estado, total
            FROM pedido
            WHERE id_usuario = %s
            ORDER BY fecha_hora DESC, id DESC
        """
        return selectDB(configDB, sql, (user_id,))

    @staticmethod
    def listar_items_por_pedido_ids(configDB, pedido_ids):
        """
        Trae items de varios pedidos (join con producto para nombre/desc/imagen).
        Devuelve:
          (id_pedido, id_producto, cantidad, precio_uni, nombre, descripcion, imagen, sabor)
        OJO: tu tabla pedido_detalle NO tiene sabor, así que lo devolvemos como NULL.
        """
        if not pedido_ids:
            return []

        placeholders = ",".join(["%s"] * len(pedido_ids))
        sql = f"""
            SELECT
                d.id_pedido,
                d.id_producto,
                d.cantidad,
                d.precio_uni,
                p.nombre,
                p.descripcion,
                p.imagen,
                NULL as sabor
            FROM pedido_detalle d
            INNER JOIN producto p ON p.id = d.id_producto
            WHERE d.id_pedido IN ({placeholders})
            ORDER BY d.id_pedido DESC, d.id DESC
        """
        return selectDB(configDB, sql, tuple(pedido_ids))

    @staticmethod
    def crear_pedido(configDB, user_id, estado, total):
        """
        Inserta cabecera pedido.
        IMPORTANTE: insertDB retorna rowcount (no last_id).
        Por eso después buscamos el último pedido del usuario.
        """
        sql = """
            INSERT INTO pedido (id, id_usuario, fecha_hora, estado, total)
            VALUES (NULL, %s, NOW(), %s, %s)
        """
        return insertDB(configDB, sql, (user_id, estado, total))

    @staticmethod
    def obtener_ultimo_pedido_id_usuario(configDB, user_id):
        sql = """
            SELECT id
            FROM pedido
            WHERE id_usuario = %s
            ORDER BY id DESC
            LIMIT 1
        """
        rows = selectDB(configDB, sql, (user_id,))
        if rows and len(rows) > 0:
            return rows[0][0]
        return None

    @staticmethod
    def crear_detalle(configDB, id_pedido, id_producto, cantidad, precio_uni):
        sql = """
            INSERT INTO pedido_detalle (id, id_pedido, id_producto, cantidad, precio_uni)
            VALUES (NULL, %s, %s, %s, %s)
        """
        return insertDB(configDB, sql, (id_pedido, id_producto, cantidad, precio_uni))

    @staticmethod
    def actualizar_estado(configDB, pedido_id, estado):
        sql = "UPDATE pedido SET estado = %s WHERE id = %s"
        return updateDB(configDB, sql, (estado, pedido_id))

    # ===== ADMIN: listar todo =====
    @staticmethod
    def listar_pedidos_admin(configDB, limit=200):
        sql = """
            SELECT p.id, p.id_usuario, p.fecha_hora, p.estado, p.total,
                   u.nombre, u.apellido, u.email, u.direccion
            FROM pedido p
            INNER JOIN usuario u ON u.id = p.id_usuario
            ORDER BY p.fecha_hora DESC, p.id DESC
            LIMIT %s
        """
        return selectDB(configDB, sql, (int(limit),))