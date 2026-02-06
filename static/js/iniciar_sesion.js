function validarEmail(idInput, idError) {
    var texto = document.getElementById(idInput).value.trim();
    var error = "";

    // Expresión regular para validar email
    var patronCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (texto === "") {
        error = "Debe ingresar un correo.";
    } else if (!patronCorreo.test(texto)) {
        error = "El formato del correo no es válido.";
    }

    var span = document.getElementById(idError);
    span.innerHTML = error;
    span.style.color = "red";

    return error === "";
}

function validarPassword(idInput, idError) {
    var pass = document.getElementById(idInput).value;
    var error = "";

    if (pass.length < 6) {
        error = "Debe tener al menos 6 caracteres.";
    } else if (!/[A-Z]/.test(pass)) {
        error = "Debe contener al menos una mayúscula.";
    } else if (!/[0-9]/.test(pass)) {
        error = "Debe contener al menos un número.";
    }

    var span = document.getElementById(idError);
    span.innerHTML = error;
    span.style.color = "red";

    return error === "";
}

function validarFormularioLogin(evento) {
    var valido = true;

    if (!validarEmail("Email", "errorEmail")) valido = false;
    if (!validarPassword("Clave", "errorClave")) valido = false;

    if (!valido) {
        evento.preventDefault();
    } else {
        usuarioEmail = document.getElementById("Email").value;
        if (typeof actualizarHeader === "function") {
            actualizarHeader();
        }
    }
}

function prepararMensajesDeError() {
    if (!document.getElementById("errorEmail")) {
        var spanEmail = document.createElement("span");
        spanEmail.id = "errorEmail";
        spanEmail.style.display = "block";
        spanEmail.style.marginTop = "4px";

        var inputEmail = document.getElementById("Email");
        inputEmail.after(spanEmail);
    }

    if (!document.getElementById("errorClave")) {
        var spanClave = document.createElement("span");
        spanClave.id = "errorClave";
        spanClave.style.display = "block";
        spanClave.style.marginTop = "4px";

        var inputClave = document.getElementById("Clave");
        inputClave.after(spanClave);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    prepararMensajesDeError();
    var formulario = document.querySelector("form");
    formulario.addEventListener("submit", validarFormularioLogin);
});