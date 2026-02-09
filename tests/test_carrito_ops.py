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
    # Login
    user = UsuarioModel.login(POWERLAB_DB, "ignacioledo@uca.edu.ar", "1234")
    if not user:
        print("LOGIN FAIL")
        return
    id_usuario = user[0]

    # carrito
    carrito = PedidoModel.obtener_carrito_activo(POWERLAB_DB, id_usuario)
    if not carrito:
        PedidoModel.crear_carrito(POWERLAB_DB, id_usuario)
        carrito = PedidoModel.obtener_carrito_activo(POWERLAB_DB, id_usuario)

    id_pedido = carrito[0]
    print("CARRITO:", id_pedido)

    # producto id 1
    p = ProductoModel.obtener_por_id(POWERLAB_DB, 1)
    if not p:
        print("NO PROD 1")
        return
    id_producto = p[0]
    precio = p[4]

    # asegurar que exista un item (lo agregamos)
    PedidoDetalleModel.agregar_item(POWERLAB_DB, id_pedido, id_producto, 1, precio)
    print("AGREGO item x1")

    # actualizar cantidad a 3
    PedidoDetalleModel.actualizar_cantidad(POWERLAB_DB, id_pedido, id_producto, 3)
    print("UPDATE cantidad -> 3")

    # recalcular total
    total = PedidoDetalleModel.calcular_total_pedido(POWERLAB_DB, id_pedido)
    PedidoModel.actualizar_total(POWERLAB_DB, id_pedido, total)
    print("TOTAL:", total)

    # eliminar item
    PedidoDetalleModel.eliminar_item(POWERLAB_DB, id_pedido, id_producto)
    print("DELETE item")

    # recalcular total
    total = PedidoDetalleModel.calcular_total_pedido(POWERLAB_DB, id_pedido)
    PedidoModel.actualizar_total(POWERLAB_DB, id_pedido, total)
    print("TOTAL:", total)

    # vaciar carrito
    PedidoDetalleModel.vaciar_pedido(POWERLAB_DB, id_pedido)
    print("VACIAR carrito")

    # total final
    total = PedidoDetalleModel.calcular_total_pedido(POWERLAB_DB, id_pedido)
    PedidoModel.actualizar_total(POWERLAB_DB, id_pedido, total)
    print("TOTAL FINAL:", total)

if __name__ == "__main__":
    main()