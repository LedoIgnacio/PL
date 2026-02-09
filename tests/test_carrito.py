import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.config_db import POWERLAB_DB
from app.models.usuario_model import UsuarioModel
from app.models.producto_model import ProductoModel
from app.models.pedido_model import PedidoModel
from app.models.pedido_detalle_model import PedidoDetalleModel

def main():
    # 1) Login para obtener id_usuario
    user = UsuarioModel.login(POWERLAB_DB, "ignacioledo@uca.edu.ar", "1234")
    if not user:
        print("LOGIN FAIL")
        return
    id_usuario = user[0]
    print("USUARIO ID:", id_usuario)

    # 2) Obtener o crear carrito
    carrito = PedidoModel.obtener_carrito_activo(POWERLAB_DB, id_usuario)
    if not carrito:
        PedidoModel.crear_carrito(POWERLAB_DB, id_usuario)
        carrito = PedidoModel.obtener_carrito_activo(POWERLAB_DB, id_usuario)

    id_pedido = carrito[0]
    print("CARRITO ID:", id_pedido)

    # 3) Elegir un producto y agregarlo
    p = ProductoModel.obtener_por_id(POWERLAB_DB, 1)
    if not p:
        print("NO EXISTE PRODUCTO ID 1")
        return

    id_producto = p[0]
    precio = p[4]
    PedidoDetalleModel.agregar_item(POWERLAB_DB, id_pedido, id_producto, 2, precio)
    print("ITEM AGREGADO:", id_producto, "x2")

    # 4) Recalcular total y actualizar pedido
    total = PedidoDetalleModel.calcular_total_pedido(POWERLAB_DB, id_pedido)
    PedidoModel.actualizar_total(POWERLAB_DB, id_pedido, total)
    print("TOTAL ACTUALIZADO:", total)

    # 5) Mostrar detalle
    items = PedidoDetalleModel.listar_por_pedido(POWERLAB_DB, id_pedido)
    print("ITEMS:", len(items))
    for it in items[:5]:
        # (pd.id, pd.id_pedido, pd.id_producto, cantidad, precio_uni, nombre, marca)
        print(it)

if __name__ == "__main__":
    main()