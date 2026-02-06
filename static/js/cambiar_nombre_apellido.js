function validarNombreApellido(idInput, idError) {
    var texto = document.getElementById(idInput).value.trim();
    var error = "";

    if (texto === "") {
        error = "Este campo es obligatorio.";
    } else if (texto.charAt(0) !== texto.charAt(0).toUpperCase()) {
        error = "Debe comenzar con mayúscula.";
    }
    var span = document.getElementById(idError);
    span.innerHTML = error;
    span.style.color = "red";

    return error === "";
}

function validarFormularioNombreApellido(evento) {
    var valido = true;
    if (!validarNombreApellido("NombreApellido", "errorNombreApellido")) valido = false;

    if (!valido) {
        evento.preventDefault();
    } else {
        evento.preventDefault();
        var mensaje = document.getElementById("errorNombreApellido");
        mensaje.style.color = "green";
        mensaje.innerText = "Tu nombre y apellido fueron actualizados correctamente.";
        document.querySelector("form").reset();
    }
}

function prepararMensajesDeError() {
    if (!document.getElementById("errorNombreApellido")) {
        var span = document.createElement("span");
        span.id = "errorNombreApellido";
        document.getElementById("NombreApellido").after(span);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    prepararMensajesDeError();
    var formulario = document.querySelector("form");
    formulario.addEventListener("submit", validarFormularioNombreApellido);
});
