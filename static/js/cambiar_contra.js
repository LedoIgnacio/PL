function validarEmail(idInput, idError) {
    var texto = document.getElementById(idInput).value.trim();
    var error = "";

    if (texto === "") {
        error = "Debe ingresar un correo.";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(texto)) {
        error = "Debe ingresar un correo válido.";
    }

    var span = document.getElementById(idError);
    span.innerText = error;
    span.style.color = "red";

    return error === "";
}

function validarFormulario(evento) {
    var valido = validarEmail("mail", "errorMail");

    if (!valido) {
        evento.preventDefault();
    } else {
        evento.preventDefault();
        var span = document.getElementById("errorMail");
        span.style.color = "green";
        span.innerText = "Se envió un email para cambiar tu contraseña.";
        document.querySelector("form").reset();
    }
}

function prepararMensajesDeError() {
    if (!document.getElementById("errorMail")) {
        var span = document.createElement("span");
        span.id = "errorMail";
        span.style.display = "block";
        span.style.marginTop = "5px";
        document.getElementById("mail").after(span);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    prepararMensajesDeError();
    var formulario = document.getElementById("formCambiarContrasena");
    formulario.addEventListener("submit", validarFormulario);
});
