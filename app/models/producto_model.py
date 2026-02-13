from app._mysql_db import selectDB


class ProductoModel:

    # =========================
    # LISTADOS "CRUD" (sin agrupar)
    # =========================
    @staticmethod
    def listar_todos(configDB):
        sql = """
            SELECT id, nombre, marca, descripcion, precio, stock, imagen, categoria, sabor
            FROM producto
            ORDER BY id DESC
        """
        return selectDB(configDB, sql)

    @staticmethod
    def listar_por_categoria(configDB, categoria):
        sql = """
            SELECT id, nombre, marca, descripcion, precio, stock, imagen, categoria, sabor
            FROM producto
            WHERE categoria = %s
            ORDER BY id DESC
        """
        return selectDB(configDB, sql, (categoria,))

    @staticmethod
    def obtener_por_id(configDB, id_producto):
        sql = """
            SELECT id, nombre, marca, descripcion, precio, stock, imagen, categoria, sabor
            FROM producto
            WHERE id = %s
            LIMIT 1
        """
        res = selectDB(configDB, sql, (id_producto,))
        return res[0] if res else None

    # =========================
    # CATÁLOGO "ÚNICO" (sin repetidos)
    # Agrupa por nombre+marca
    # =========================
    @staticmethod
    def listar_unicos(configDB, categoria=None, marca=None, sabor=None):
        """
        Devuelve 1 fila por (nombre, marca).
        - id = MIN(id) (id representativo)
        - stock = SUM(stock) (stock total entre sabores)
        - imagen = MIN(imagen) (una imagen representativa)
        - categoria/sabor = MIN(...) (solo representativo)
        """
        sql = """
            SELECT
                MIN(id)            AS id,
                nombre,
                marca,
                MIN(descripcion)   AS descripcion,
                MIN(precio)        AS precio,
                SUM(stock)         AS stock,
                MIN(imagen)        AS imagen,
                MIN(categoria)     AS categoria,
                MIN(sabor)         AS sabor
            FROM producto
            WHERE 1=1
        """
        params = []

        if categoria:
            sql += " AND categoria = %s"
            params.append(categoria)

        if marca:
            sql += " AND marca = %s"
            params.append(marca)

        if sabor:
            sql += " AND sabor = %s"
            params.append(sabor)

        sql += """
            GROUP BY nombre, marca
            ORDER BY id DESC
        """

        if params:
            return selectDB(configDB, sql, tuple(params))
        return selectDB(configDB, sql)

    # =========================
    # ITEM "ÚNICO" + SABORES DISPONIBLES
    # =========================
    @staticmethod
    def obtener_unico_por_id(configDB, id_producto):
        """
        Dado un id (por ejemplo el MIN(id) del catálogo),
        devuelve el producto "único" (agregado por nombre+marca).
        """
        # 1) saco nombre+marca del id
        base = selectDB(
            configDB,
            "SELECT nombre, marca FROM producto WHERE id = %s LIMIT 1",
            (id_producto,)
        )
        if not base:
            return None

        nombre, marca = base[0][0], base[0][1]

        # 2) devuelvo el agregado para ese nombre+marca
        sql = """
            SELECT
                MIN(id)            AS id,
                nombre,
                marca,
                MIN(descripcion)   AS descripcion,
                MIN(precio)        AS precio,
                SUM(stock)         AS stock,
                MIN(imagen)        AS imagen,
                MIN(categoria)     AS categoria
            FROM producto
            WHERE nombre = %s AND marca = %s
            GROUP BY nombre, marca
            LIMIT 1
        """
        res = selectDB(configDB, sql, (nombre, marca))
        return res[0] if res else None

    @staticmethod
    def listar_sabores_por_id(configDB, id_producto):
        """
        Devuelve todos los sabores disponibles para el producto "único"
        (mismo nombre+marca del id_producto).
        """
        base = selectDB(
            configDB,
            "SELECT nombre, marca FROM producto WHERE id = %s LIMIT 1",
            (id_producto,)
        )
        if not base:
            return []

        nombre, marca = base[0][0], base[0][1]

        sql = """
            SELECT DISTINCT sabor
            FROM producto
            WHERE nombre = %s AND marca = %s AND sabor IS NOT NULL AND sabor <> ''
            ORDER BY sabor ASC
        """
        return selectDB(configDB, sql, (nombre, marca))