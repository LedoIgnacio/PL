var usuarioNombre = null;
var usuarioEmail = null;
var esAdmin = false; //si el usuario es admin

function actualizarHeader() {
    var nodoLogin = document.querySelector(".Inicio-sesion");
    var padre = nodoLogin.parentNode;

    if (usuarioNombre !== null || usuarioEmail !== null) {
        var nuevoSpan = document.createElement("span");
        nuevoSpan.className = "Inicio-sesion";

        if (esAdmin) {
            if (usuarioNombre !== null) {
                nuevoSpan.innerHTML = "ADMIN: Hola " + usuarioNombre;
            } else {
                nuevoSpan.innerHTML = "ADMIN: Hola " + usuarioEmail;
            }
        } else {
            if (usuarioNombre !== null) {
                nuevoSpan.innerHTML = "Hola " + usuarioNombre;
            } else {
                nuevoSpan.innerHTML = "Hola " + usuarioEmail;
            }
        }

        padre.replaceChild(nuevoSpan, nodoLogin);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    actualizarHeader();
});