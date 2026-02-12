from app._mysql_db import selectDB

class ProductoModel:

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
    def listar_unicos(configDB):
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
            GROUP BY nombre, marca
            ORDER BY id DESC
        """
        return selectDB(configDB, sql)

    @staticmethod
    def listar_unicos_por_categoria(configDB, categoria):
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
            WHERE categoria = %s
            GROUP BY nombre, marca
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
    
    @staticmethod
    def listar_unicos_por_sabor(configDB, sabor):
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
            WHERE sabor = %s
            GROUP BY nombre, marca
            ORDER BY id DESC
        """
        return selectDB(configDB, sql, (sabor,))

    @staticmethod
    def listar_unicos_por_categoria_y_sabor(configDB, categoria, sabor):
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
            WHERE categoria = %s AND sabor = %s
            GROUP BY nombre, marca
            ORDER BY id DESC
        """
        return selectDB(configDB, sql, (categoria, sabor))