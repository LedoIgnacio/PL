from flask import render_template, request, redirect, url_for, session, jsonify
from app.config_db import POWERLAB_DB
from app.models.usuario_model import UsuarioModel
from app.models.producto_model import ProductoModel


def home():
    return render_template("public/index.html")


def auth_registrarse():
    return render_template("auth/registrarse.html")


def profile_perfil():
    if "user_id" not in session:
        return redirect(url_for("login_get"))
    return render_template("profile/perfil.html")


def shop_productos():
    # /productos?categoria=proteina&marca=ena&sabor=chocolate
    categoria = (request.args.get("categoria") or "").strip().lower()
    marca = (request.args.get("marca") or "").strip().lower()
    sabor = (request.args.get("sabor") or "").strip().lower()

    # normalizar vacíos
    if categoria in ("", "todos"):
        categoria = None
    if marca in ("", "todas"):
        marca = None
    if sabor in ("", "todas"):
        sabor = None

    # 1 SOLO query (el model ya arma WHERE dinámico)
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


def shop_item(id_producto):
    producto = ProductoModel.obtener_unico_por_id(POWERLAB_DB, id_producto)
    if not producto:
        return redirect(url_for("productos"))

    sabores_rows = ProductoModel.listar_sabores_por_id(POWERLAB_DB, id_producto)
    sabores = [row[0] for row in sabores_rows] if sabores_rows else []

    # por si querés que llegue preseleccionado desde la URL
    sabor_sel = (request.args.get("sabor") or "").strip().lower() or None
    if sabor_sel and sabor_sel not in [s.lower() for s in sabores]:
        sabor_sel = None

    return render_template("shop/item.html", p=producto, sabores=sabores, sabor_sel=sabor_sel)


def shop_carrito():
    if "user_id" not in session:
        return redirect(url_for("login_get"))
    return render_template("shop/carrito.html")


def shop_pago():
    if "user_id" not in session:
        return redirect(url_for("login_get"))
    return render_template("shop/pago.html")


def shop_mis_compras():
    if "user_id" not in session:
        return redirect(url_for("login_get"))
    return render_template("shop/mis_compras.html")


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


def admin_carga():
    if "user_id" not in session or session.get("user_tipo") != "admin":
        return redirect(url_for("admin_login"))
    return render_template("admin/carga_admin.html")


def admin_estado_compra():
    if "user_id" not in session or session.get("user_tipo") != "admin":
        return redirect(url_for("admin_login"))
    return render_template("admin/estado_compra.html")


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