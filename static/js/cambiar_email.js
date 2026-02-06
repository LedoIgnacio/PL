function validarEmail(idInput, idError) {
    var email = document.getElementById(idInput).value.trim();
    var error = "";

    if (email === "") {
        error = "Debe ingresar un correo.";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        error = "El correo no es válido.";
    }

    document.getElementById(idError).innerHTML = error;
    document.getElementById(idError).style.color = "red";

    return error === "";
}

function validarFormularioEmail(evento) {
    var valido = true;
    if (!validarEmail("Email", "errorEmail")) valido = false;

    if (!valido) {
        evento.preventDefault();
    } else {
        evento.preventDefault();
        var mensaje = document.getElementById("errorEmail");
        mensaje.style.color = "green";
        mensaje.innerText = "Tu correo fue actualizado correctamente.";
        document.querySelector("form").reset();
    }
}

function prepararMensajesDeError() {
    if (!document.getElementById("errorEmail")) {
        var span = document.createElement("span");
        span.id = "errorEmail";
        document.getElementById("Email").after(span);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    prepararMensajesDeError();
    var formulario = document.querySelector("form");
    formulario.addEventListener("submit", validarFormularioEmail);
});
