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

    # Obtener o crear carrito
    carrito = PedidoModel.obtener_carrito_activo(POWERLAB_DB, id_usuario)
    if not carrito:
        PedidoModel.crear_carrito(POWERLAB_DB, id_usuario)
        carrito = PedidoModel.obtener_carrito_activo(POWERLAB_DB, id_usuario)

    id_pedido = carrito[0]
    print("CARRITO:", id_pedido)

    # Asegurar al menos 1 item (agrego producto id 1)
    p = ProductoModel.obtener_por_id(POWERLAB_DB, 1)
    if not p:
        print("NO PROD 1")
        return
    PedidoDetalleModel.agregar_item(POWERLAB_DB, id_pedido, p[0], 1, p[4])

    # Recalcular total y actualizar
    total = PedidoDetalleModel.calcular_total_pedido(POWERLAB_DB, id_pedido)
    PedidoModel.actualizar_total(POWERLAB_DB, id_pedido, total)
    print("TOTAL CARRITO:", total)

    # Checkout: cerrar carrito -> en_proceso
    PedidoModel.cerrar_carrito_en_proceso(POWERLAB_DB, id_pedido)
    print("CHECKOUT OK -> en_proceso")

    # Mis compras: listar pedidos no-carrito
    compras = PedidoModel.listar_por_usuario(POWERLAB_DB, id_usuario)
    print("MIS COMPRAS:", len(compras))
    for ped in compras[:5]:
        # pedido: (id, id_usuario, fecha_hora, estado, total)
        print("PEDIDO:", ped[0], ped[3], ped[4])

if __name__ == "__main__":
    main()