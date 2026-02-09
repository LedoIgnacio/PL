import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.config_db import POWERLAB_DB
from app.models.pedido_model import PedidoModel
from app.models.pedido_detalle_model import PedidoDetalleModel

def main():
    # 1) listar pedidos
    pedidos = PedidoModel.listar_todos(POWERLAB_DB)
    print("PEDIDOS:", len(pedidos))
    if not pedidos:
        return

    # pedido: (id, id_usuario, fecha_hora, estado, total)
    p = pedidos[0]
    id_pedido = p[0]
    print("PRIMERO:", id_pedido, p[3], p[4])

    # 2) ver detalle del pedido
    items = PedidoDetalleModel.listar_por_pedido(POWERLAB_DB, id_pedido)
    print("DETALLE ITEMS:", len(items))
    for it in items[:5]:
        print(it)

    # 3) listar solo en_proceso
    en_proc = PedidoModel.listar_por_estado(POWERLAB_DB, "en_proceso")
    print("EN_PROCESO:", len(en_proc))

    # 4) cambiar estado del primero si está en_proceso -> entregado (demo)
    if p[3] == "en_proceso":
        PedidoModel.cambiar_estado(POWERLAB_DB, id_pedido, "entregado")
        print("CAMBIADO A ENTREGADO:", id_pedido)

if __name__ == "__main__":
    main()