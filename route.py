from controller import (
    home,
    auth_registrarse,
    auth_login_get,
    auth_login_post,
    auth_logout,
    profile_perfil,
    shop_productos,
    shop_carrito,
    shop_pago,
    shop_mis_compras,
    admin_login_get,
    admin_login_post,
    admin_carga,
    admin_estado_compra,
    auth_login_api,
    auth_registrarse_api,
    shop_item,
)

def route(app):

    @app.route("/", methods=["GET"])
    def index():
        return home()

    @app.route("/registrarse", methods=["GET"])
    def registrarse():
        return auth_registrarse()

    @app.route("/login", methods=["GET"])
    def login_get():
        return auth_login_get()

    @app.route("/login", methods=["POST"])
    def login_post():
        return auth_login_post()

    @app.route("/perfil", methods=["GET"])
    def perfil():
        return profile_perfil()

    @app.route("/productos", methods=["GET"])
    def productos():
        return shop_productos()

    @app.route("/carrito", methods=["GET"])
    def carrito():
        return shop_carrito()

    @app.route("/pago", methods=["GET"])
    def pago():
        return shop_pago()

    @app.route("/mis-compras", methods=["GET"])
    def mis_compras():
        return shop_mis_compras()

    @app.route("/api/login", methods=["POST"])
    def login_api():
        return auth_login_api()

    @app.route("/api/registrarse", methods=["POST"])
    def registrarse_api():
        return auth_registrarse_api()

    @app.route("/logout", endpoint="logout")
    def logout_route():
        return auth_logout()

    @app.route("/admin/login", methods=["GET"])
    def admin_login():
        return admin_login_get()

    @app.route("/admin/login", methods=["POST"])
    def admin_login_post_route():
        return admin_login_post()

    @app.route("/admin/carga", methods=["GET"])
    def admin_carga_route():
        return admin_carga()

    @app.route("/admin/estado-compra", methods=["GET"])
    def admin_estado_compra_route():
        return admin_estado_compra()

    @app.route("/item/<int:id_producto>", methods=["GET"], endpoint="item")
    def item_route(id_producto):
        return shop_item(id_producto)