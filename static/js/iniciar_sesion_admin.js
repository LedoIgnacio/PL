function mostrarError(idInput, mensaje) {
    var span = document.getElementById("error-" + idInput);
    span.innerText = mensaje;
    span.style.color = "red";
}

function limpiarError(idInput) {
    var span = document.getElementById("error-" + idInput);
    span.innerText = "";
}

function mostrarExito(mensaje) {
    var mensajeFinal = document.getElementById("mensajeExito");
    mensajeFinal.innerText = mensaje;
    mensajeFinal.style.color = "green";
}

function validarEmail() {
    var texto = document.getElementById("Email").value.trim();
    var expresion = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var error = "";

    if (texto === "") {
        error = "Debe ingresar un correo.";
    } else if (!expresion.test(texto)) {
        error = "Correo inválido.";
    }

    if (error !== "") {
        mostrarError("Email", error);
        return false;
    }

    limpiarError("Email");
    return true;
}

function validarPassword() {
    var pass = document.getElementById("Clave").value;
    var error = "";

    if (pass === "") {
        error = "Debe ingresar una contraseña.";
    } else if (pass.length < 6) {
        error = "Debe tener al menos 6 caracteres.";
    } else if (!/[A-Z]/.test(pass)) {
        error = "Debe contener al menos una mayúscula.";
    } else if (!/[0-9]/.test(pass)) {
        error = "Debe contener al menos un número.";
    }

    if (error !== "") {
        mostrarError("Clave", error);
        return false;
    }

    limpiarError("Clave");
    return true;
}

function validarFormularioAdminLogin(evento) {
    evento.preventDefault();

    var ok1 = validarEmail();
    var ok2 = validarPassword();

    if (ok1 && ok2) {
        usuarioEmail = document.getElementById("Email").value;
        esAdmin = true;

        if (typeof actualizarHeader === "function") {
            actualizarHeader();
        }

        mostrarExito("Inicio de sesión exitoso.");
        document.querySelector("form").reset();
    }
}

function prepararMensajesDeError() {
    var ids = ["Email", "Clave"];
    for (var i = 0; i < ids.length; i++) {
        if (!document.getElementById("error-" + ids[i])) {
            var span = document.createElement("span");
            span.id = "error-" + ids[i];
            span.style.display = "block";
            span.style.marginTop = "4px";
            document.getElementById(ids[i]).after(span);
        }
    }

    if (!document.getElementById("mensajeExito")) {
        var exito = document.createElement("span");
        exito.id = "mensajeExito";
        exito.style.display = "block";
        exito.style.marginTop = "10px";
        var boton = document.querySelector("button");
        boton.after(exito);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    prepararMensajesDeError();
    var formulario = document.querySelector("form");
    formulario.addEventListener("submit", validarFormularioAdminLogin);
});