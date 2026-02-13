from flask import render_template, request, redirect, url_for, session, jsonify
from app.config_db import POWERLAB_DB
from app.models.usuario_model import UsuarioModel
from app.models.producto_model import ProductoModel

# ============================================================
# CARRITO (SESSION) - estilo simple, sin DB todavía
# ============================================================

def _get_cart():
    """
    Estructura en session:
    session["cart"] = {
        "<id_producto>:<sabor_lower>": {
            "key": str,
            "producto_id": int,
            "sabor": str,
            "nombre": str,
            "marca": str,
            "precio": float|int,
            "imagen": str,
            "cantidad": int
        },
        ...
    }
    """
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
        # compat: si quedó algo viejo con qty, lo toma igual
        cant = it.get("cantidad", it.get("qty", 1))

        # normalizo para adelante
        it["cantidad"] = cant
        if "qty" in it:
            it.pop("qty", None)

        precio = it.get("precio", 0)
        total += (precio * cant)
        count += cant

    return items, total, count

def _img_url(img_value):
    """
    Normaliza imagen para que el HTML pueda usarla directo.
    Si en DB guardás:
      - URL completa => la usa
      - nombre de archivo => arma /static/img/productos/<archivo>
    """
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
    # /productos?categoria=proteina&marca=ena&sabor=chocolate
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
# CARRITO (PÁGINA)
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

    # dirección desde DB
    user_id = session.get("user_id")
    user = UsuarioModel.obtener_por_id(POWERLAB_DB, user_id)  # AJUSTÁ si tu método se llama distinto

    # ===== AJUSTAR ÍNDICE DE DIRECCIÓN =====
    # Depende del SELECT de tu UsuarioModel.obtener_por_id()
    # Ejemplo típico: (id, nombre, apellido, email, telefono, direccion, pass, tipo_usuario)
    # Entonces direccion sería user[5]
    direccion = None
    if user:
        try:
            direccion = user[5]  # <-- CAMBIÁ ESTE ÍNDICE SI TU TUPLA ES DISTINTA
        except:
            direccion = None

    return render_template("shop/pago.html", items=items, total=total, count=count, direccion=direccion)


def shop_mis_compras():
    if "user_id" not in session:
        return redirect(url_for("login_get"))
    return render_template("shop/mis_compras.html")


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
    return render_template("admin/estado_compra.html")

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
# API CARRITO (AJAX) - JSON
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
        # producto: (id, nombre, marca, descripcion, precio, stock, imagen, categoria)
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

    # normalizo cantidad por si viniera viejo
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