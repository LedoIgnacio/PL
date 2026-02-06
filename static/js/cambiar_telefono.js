function validarTelefono(idInput, idError) {
    var telefono = document.getElementById(idInput).value.trim();
    var error = "";

    if (telefono === "") {
        error = "Debe ingresar un número de teléfono.";
    } else if (!/^\d{8,15}$/.test(telefono)) {
        error = "El teléfono debe tener solo números y entre 8 y 15 dígitos.";
    }

    var spanError = document.getElementById(idError);
    spanError.innerHTML = error;
    spanError.style.color = "red";

    return error === "";
}

function validarFormularioTelefono(evento) {
    var valido = true;
    if (!validarTelefono("Telefono", "errorTelefono")) valido = false;

    if (!valido) {
        evento.preventDefault();
    } else {
        evento.preventDefault();
        var mensaje = document.getElementById("errorTelefono");
        mensaje.style.color = "green";
        mensaje.innerText = "Tu número de teléfono fue actualizado correctamente.";
        document.querySelector("form").reset();
    }
}

function prepararMensajesDeError() {
    if (!document.getElementById("errorTelefono")) {
        var span = document.createElement("span");
        span.id = "errorTelefono";
        document.getElementById("Telefono").after(span);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    prepararMensajesDeError();
    var formulario = document.querySelector("form");
    formulario.addEventListener("submit", validarFormularioTelefono);
});
