from flask import render_template, request, redirect, url_for, session, jsonify
from app.config_db import POWERLAB_DB
from app.models.usuario_model import UsuarioModel
from app.models.producto_model import ProductoModel
from app.models.pedido_model import PedidoModel


# ============================================================
# CARRITO (SESSION)
# ============================================================

def _get_cart():
    return session.get("cart", {})

def _set_cart(cart):
    session["cart"] = cart
    session.modified = True

def _cart_totals(cart):
    """
    Devuelve SIEMPRE 3 valores:
    items: lista de dicts
    total: suma precio*cantidad
    count: suma cantidades (contador del carrito)
    """
    items = list(cart.values())
    total = 0
    count = 0

    for it in items:
        cant = it.get("cantidad", it.get("qty", 1))

        # normalizo para adelante
        it["cantidad"] = cant
        it.pop("qty", None)

        precio = it.get("precio", 0)
        total += (precio * cant)
        count += cant

    return items, total, count

def _img_url(img_value):
    img = (img_value or "").strip()
    if img.startswith("http"):
        return img
    return "/static/img/productos/" + img

def _require_login_json():
    if "user_id" not in session:
        return jsonify({"ok": False, "msg": "No logueado", "redirect": "/login"}), 401
    return None


# =========================
# PÁGINAS GENERALES
# =========================

def home():
    return render_template("public/index.html")

def auth_registrarse():
    return render_template("auth/registrarse.html")

def profile_perfil():
    if "user_id" not in session:
        return redirect(url_for("login_get"))
    return render_template("profile/perfil.html")


# =========================
# CATÁLOGO
# =========================

def shop_productos():
    categoria = (request.args.get("categoria") or "").strip().lower()
    marca = (request.args.get("marca") or "").strip().lower()
    sabor = (request.args.get("sabor") or "").strip().lower()

    if categoria in ("", "todos"):
        categoria = None
    if marca in ("", "todas"):
        marca = None
    if sabor in ("", "todas"):
        sabor = None

    productos = ProductoModel.listar_unicos(
        POWERLAB_DB,
        categoria=categoria,
        marca=marca,
        sabor=sabor
    )

    return render_template(
        "shop/productos.html",
        productos=productos,
        categoria=categoria,
        marca=marca,
        sabor=sabor
    )


# =========================
# ITEM
# =========================

def shop_item(id_producto):
    producto = ProductoModel.obtener_unico_por_id(POWERLAB_DB, id_producto)
    if not producto:
        return redirect(url_for("productos"))

    sabores_rows = ProductoModel.listar_sabores_por_id(POWERLAB_DB, id_producto)
    sabores = [row[0] for row in sabores_rows] if sabores_rows else []

    sabor_sel = (request.args.get("sabor") or "").strip()
    if sabor_sel and sabor_sel.lower() not in [s.lower() for s in sabores]:
        sabor_sel = None

    return render_template("shop/item.html", p=producto, sabores=sabores, sabor_sel=sabor_sel)


# =========================
# CARRITO (PÁGINAS)
# =========================

def shop_carrito():
    if "user_id" not in session:
        return redirect(url_for("login_get"))

    cart = _get_cart()
    items, total, count = _cart_totals(cart)

    return render_template("shop/carrito.html", items=items, total=total, count=count)


def shop_pago():
    if "user_id" not in session:
        return redirect(url_for("login_get"))

    cart = _get_cart()
    items, total, count = _cart_totals(cart)

    user_id = session.get("user_id")
    user = UsuarioModel.obtener_por_id(POWERLAB_DB, user_id)  # AJUSTÁ si tu método se llama distinto

    # según tu INSERT: usuario(id,nombre,apellido,email,telefono,direccion,pass,tipo_usuario)
    direccion = None
    if user:
        try:
            direccion = user[5]
        except:
            direccion = None

    return render_template("shop/pago.html", items=items, total=total, count=count, direccion=direccion)


def shop_mis_compras():
    if "user_id" not in session:
        return redirect(url_for("login_get"))

    user_id = session.get("user_id")

    pedidos_rows = PedidoModel.listar_pedidos_por_usuario(POWERLAB_DB, user_id) or []

    pedidos = []
    pedido_ids = []

    for row in pedidos_rows:
        # (id, id_usuario, fecha_hora, estado, total)
        p = {
            "id": row[0],
            "usuario_id": row[1],
            "fecha": row[2],
            "estado": row[3],
            "total": row[4],
            "items": []
        }
        pedidos.append(p)
        pedido_ids.append(row[0])

    items_rows = PedidoModel.listar_items_por_pedido_ids(POWERLAB_DB, pedido_ids) or []
    pedidos_by_id = {p["id"]: p for p in pedidos}

    for it in items_rows:
        # (id_pedido, id_producto, cantidad, precio_uni, nombre, descripcion, imagen, sabor)
        pedido_id = it[0]
        if pedido_id in pedidos_by_id:
            pedidos_by_id[pedido_id]["items"].append({
                "producto_id": it[1],
                "cantidad": it[2],
                "precio": it[3],
                "nombre": it[4],
                "descripcion": it[5],
                "imagen": _img_url(it[6]),
                "sabor": it[7]  # None
            })

    cart = _get_cart()
    _, _, count = _cart_totals(cart)

    return render_template("shop/mis_compras.html", pedidos=pedidos, count=count)


# =========================
# AUTH
# =========================

def auth_login_get():
    return render_template("auth/login.html")

def auth_login_post():
    email = request.form.get("email")
    password = request.form.get("pass")

    user = UsuarioModel.login(POWERLAB_DB, email, password)

    if user:
        session["user_id"] = user[0]
        session["user_nombre"] = user[1]
        session["user_tipo"] = user[7]
        return redirect(url_for("index"))

    return render_template("auth/login.html", error="Email o contraseña incorrectos")

def auth_logout():
    session.clear()
    return redirect(url_for("index"))


# =========================
# ADMIN
# =========================

def admin_carga():
    if "user_id" not in session or session.get("user_tipo") != "admin":
        return redirect(url_for("admin_login"))
    return render_template("admin/carga_admin.html")

def admin_estado_compra():
    if "user_id" not in session or session.get("user_tipo") != "admin":
        return redirect(url_for("admin_login"))

    pedidos_rows = PedidoModel.listar_pedidos_admin(POWERLAB_DB, limit=200) or []

    pedidos = []
    pedido_ids = []

    for r in pedidos_rows:
        # (id, id_usuario, fecha_hora, estado, total, nombre, apellido, email, direccion)
        p = {
            "id": r[0],
            "usuario_id": r[1],
            "fecha": r[2],
            "estado": r[3],
            "total": r[4],
            "usuario_nombre": r[5],
            "usuario_apellido": r[6],
            "usuario_email": r[7],
            "usuario_direccion": r[8],
            "items": []
        }
        pedidos.append(p)
        pedido_ids.append(r[0])

    items_rows = PedidoModel.listar_items_por_pedido_ids(POWERLAB_DB, pedido_ids) or []
    pedidos_by_id = {p["id"]: p for p in pedidos}

    for it in items_rows:
        # (id_pedido, id_producto, cantidad, precio_uni, nombre, descripcion, imagen, sabor)
        pid = it[0]
        if pid in pedidos_by_id:
            pedidos_by_id[pid]["items"].append({
                "producto_id": it[1],
                "cantidad": it[2],
                "precio": it[3],
                "nombre": it[4],
                "descripcion": it[5],
                "imagen": _img_url(it[6]),
                "sabor": it[7],
            })

    # contador carrito en header (si querés mostrarlo también en admin)
    cart = _get_cart()
    _, _, count = _cart_totals(cart)

    return render_template("admin/estado_compra.html", pedidos=pedidos, count=count)
def admin_login_get():
    return render_template("admin/login_admin.html")

def admin_login_post():
    email = request.form.get("email")
    password = request.form.get("pass")

    user = UsuarioModel.login(POWERLAB_DB, email, password)

    if user and user[7] == "admin":
        session["user_id"] = user[0]
        session["user_nombre"] = user[1]
        session["user_tipo"] = user[7]
        return redirect(url_for("admin_carga_route"))

    return render_template("admin/login_admin.html", error="Solo admins pueden entrar")


# =========================
# API AUTH (AJAX)
# =========================

def auth_login_api():
    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip()
    password = (data.get("pass") or "").strip()

    if not email or not password:
        return jsonify({"ok": False, "msg": "Faltan datos"}), 400

    user = UsuarioModel.login(POWERLAB_DB, email, password)

    if user:
        session["user_id"] = user[0]
        session["user_nombre"] = user[1]
        session["user_tipo"] = user[7]
        return jsonify({"ok": True, "redirect": "/"}), 200

    return jsonify({"ok": False, "msg": "Email o contraseña incorrectos"}), 401


def auth_registrarse_api():
    data = request.get_json(silent=True) or {}

    nombre = (data.get("nombre") or "").strip()
    apellido = (data.get("apellido") or "").strip()
    email = (data.get("email") or "").strip()
    direccion = (data.get("direccion") or "").strip()
    telefono = (data.get("telefono") or "").strip()
    password = (data.get("pass") or "").strip()
    password2 = (data.get("pass2") or "").strip()

    if not nombre or not apellido or not email or not direccion or not password or not password2:
        return jsonify({"ok": False, "msg": "Faltan datos obligatorios"}), 400

    if password != password2:
        return jsonify({"ok": False, "msg": "Las contraseñas no coinciden"}), 400

    if telefono == "":
        telefono = None

    ok = UsuarioModel.crear_usuario(POWERLAB_DB, nombre, apellido, email, telefono, direccion, password)

    if ok:
        return jsonify({"ok": True, "redirect": "/login"}), 200

    return jsonify({"ok": False, "msg": "No se pudo registrar (email duplicado o error DB)"}), 409


# ============================================================
# API CARRITO (AJAX)
# ============================================================

def cart_get_api():
    chk = _require_login_json()
    if chk:
        return chk

    cart = _get_cart()
    items, total, count = _cart_totals(cart)
    return jsonify({"ok": True, "items": items, "total": total, "count": count}), 200


def cart_add_api():
    chk = _require_login_json()
    if chk:
        return chk

    data = request.get_json(silent=True) or {}
    id_producto = int(data.get("id_producto") or 0)
    sabor = (data.get("sabor") or "").strip()

    if id_producto <= 0 or not sabor:
        return jsonify({"ok": False, "msg": "Faltan datos (id_producto/sabor)"}), 400

    producto = ProductoModel.obtener_unico_por_id(POWERLAB_DB, id_producto)
    if not producto:
        return jsonify({"ok": False, "msg": "Producto inexistente"}), 404

    sabores_rows = ProductoModel.listar_sabores_por_id(POWERLAB_DB, id_producto)
    sabores = [row[0] for row in sabores_rows] if sabores_rows else []
    if sabor.lower() not in [s.lower() for s in sabores]:
        return jsonify({"ok": False, "msg": "Sabor inválido"}), 400

    cart = _get_cart()
    key = f"{id_producto}:{sabor.lower()}"

    if key in cart:
        cart[key]["cantidad"] = cart[key].get("cantidad", 1) + 1
    else:
        cart[key] = {
            "key": key,
            "producto_id": producto[0],
            "sabor": sabor,
            "nombre": producto[1],
            "marca": producto[2],
            "precio": producto[4],
            "imagen": _img_url(producto[6]),
            "cantidad": 1
        }

    _set_cart(cart)
    items, total, count = _cart_totals(cart)
    return jsonify({"ok": True, "items": items, "total": total, "count": count}), 200


def cart_update_api():
    chk = _require_login_json()
    if chk:
        return chk

    data = request.get_json(silent=True) or {}
    key = (data.get("key") or "").strip()
    action = (data.get("action") or "").strip()  # "inc" | "dec" | "set"
    qty = data.get("qty")

    cart = _get_cart()
    if not key or key not in cart:
        return jsonify({"ok": False, "msg": "Item inexistente"}), 404

    cart[key]["cantidad"] = cart[key].get("cantidad", cart[key].get("qty", 1))
    cart[key].pop("qty", None)

    if action == "set":
        try:
            qty_int = int(qty)
        except:
            return jsonify({"ok": False, "msg": "qty inválido"}), 400

        if qty_int <= 0:
            cart.pop(key, None)
        else:
            cart[key]["cantidad"] = qty_int

    elif action == "inc":
        cart[key]["cantidad"] += 1

    elif action == "dec":
        cart[key]["cantidad"] -= 1
        if cart[key]["cantidad"] <= 0:
            cart.pop(key, None)

    else:
        return jsonify({"ok": False, "msg": "action inválida"}), 400

    _set_cart(cart)
    items, total, count = _cart_totals(cart)
    return jsonify({"ok": True, "items": items, "total": total, "count": count}), 200


def cart_remove_api():
    chk = _require_login_json()
    if chk:
        return chk

    data = request.get_json(silent=True) or {}
    key = (data.get("key") or "").strip()

    cart = _get_cart()
    if key and key in cart:
        cart.pop(key, None)
        _set_cart(cart)

    items, total, count = _cart_totals(cart)
    return jsonify({"ok": True, "items": items, "total": total, "count": count}), 200


def cart_clear_api():
    chk = _require_login_json()
    if chk:
        return chk

    session.pop("cart", None)
    session.modified = True
    return jsonify({"ok": True, "items": [], "total": 0, "count": 0}), 200


# ============================================================
# FINALIZAR COMPRA (CREA PEDIDO + DETALLES)
# ============================================================

def pedido_finalizar_post():
    if "user_id" not in session:
        return redirect(url_for("login_get"))

    cart = _get_cart()
    items, total, count = _cart_totals(cart)

    if not items or count == 0:
        return redirect(url_for("carrito"))

    user_id = session.get("user_id")

    # crea pedido
    # usamos estado acorde a tu DB
    PedidoModel.crear_pedido(POWERLAB_DB, user_id, "no_pagado", total)

    pedido_id = PedidoModel.obtener_ultimo_pedido_id_usuario(POWERLAB_DB, user_id)
    if not pedido_id:
        # si falló, no vaciamos carrito
        return redirect(url_for("carrito"))

    # crea detalles
    for it in items:
        PedidoModel.crear_detalle(
            POWERLAB_DB,
            pedido_id,
            it.get("producto_id"),
            it.get("cantidad", 1),
            it.get("precio", 0)
        )

    # vacía carrito
    session.pop("cart", None)
    session.modified = True

    return redirect(url_for("mis_compras"))


# ============================================================
# API ADMIN - ACTUALIZA ESTADO PEDIDO
# ============================================================

def admin_update_estado_pedido_api():
    if "user_id" not in session or session.get("user_tipo") != "admin":
        return jsonify({"ok": False, "msg": "No autorizado"}), 403

    data = request.get_json(silent=True) or {}
    pedido_id = int(data.get("pedido_id") or 0)
    estado = (data.get("estado") or "").strip()

    if pedido_id <= 0 or not estado:
        return jsonify({"ok": False, "msg": "Faltan datos"}), 400

    estados_ok = {"no_pagado", "en_proceso", "entregado", "carrito"}
    if estado not in estados_ok:
        return jsonify({"ok": False, "msg": "Estado inválido"}), 400

    res = PedidoModel.actualizar_estado(POWERLAB_DB, pedido_id, estado)
    if res and res > 0:
        return jsonify({"ok": True}), 200

    return jsonify({"ok": False, "msg": "No se actualizó (id inexistente?)"}), 404

def admin_crear_producto_post():
    if "user_id" not in session or session.get("user_tipo") != "admin":
        return redirect(url_for("admin_login"))

    # tu form actual trae estos nombres:
    # NombreMarca, Precio, Descripcion, Descuentos, Imagen
    nombre_marca = (request.form.get("NombreMarca") or "").strip()
    descripcion = (request.form.get("Descripcion") or "").strip()
    imagen = (request.form.get("Imagen") or "").strip()

    # descuentos no existe en tu tabla producto -> lo ignoramos
    # marca y nombre: si lo mandás junto, lo separamos simple:
    # "Whey Protein - Ena" => nombre="Whey Protein", marca="Ena"
    nombre = nombre_marca
    marca = ""
    if "-" in nombre_marca:
        parts = [p.strip() for p in nombre_marca.split("-", 1)]
        nombre = parts[0]
        marca = parts[1]

    try:
        precio = int(request.form.get("Precio") or 0)
    except:
        precio = 0

    # como tu tabla producto pide: categoria y sabor (NOT NULL en tu insert masivo)
    # si no los cargás en admin, ponemos defaults simples
    categoria = "general"
    sabor = "neutro"
    stock = 50

    if not nombre or not descripcion or not imagen or precio <= 0:
        return render_template("admin/carga_admin.html", error="Faltan datos o precio inválido")

    # insert directo usando ProductoModel (si ya tenés crear_producto ahí, úsalo)
    # si NO tenés, te paso SQL acá:
    from app._mysql_db import insertDB
    sql = """
        INSERT INTO producto (id, nombre, marca, descripcion, precio, stock, imagen, categoria, sabor)
        VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    insertDB(POWERLAB_DB, sql, (nombre, marca, descripcion, precio, stock, imagen, categoria, sabor))

    return redirect(url_for("admin_carga_route"))