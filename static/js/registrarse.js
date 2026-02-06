function mostrarError(idInput, mensaje) {
    var span = document.getElementById("error-" + idInput);
    span.innerText = mensaje;
    span.style.color = "red";
}

function limpiarError(idInput) {
    var span = document.getElementById("error-" + idInput);
    span.innerText = "";
}

function validarNombre() {
    var input = document.getElementById("Nombre");
    var texto = input.value.trim();

    if (texto === "") {
        mostrarError("Nombre", "Este campo es obligatorio.");
        return false;
    } else if (texto.charAt(0) !== texto.charAt(0).toUpperCase()) {
        mostrarError("Nombre", "Debe comenzar con mayúscula.");
        return false;
    }
    limpiarError("Nombre");
    return true;
}

function validarApellido() {
    var input = document.getElementById("Apellido");
    var texto = input.value.trim();

    if (texto === "") {
        mostrarError("Apellido", "Este campo es obligatorio.");
        return false;
    } else if (texto.charAt(0) !== texto.charAt(0).toUpperCase()) {
        mostrarError("Apellido", "Debe comenzar con mayúscula.");
        return false;
    }
    limpiarError("Apellido");
    return true;
}

function validarDireccion() {
    var input = document.getElementById("Direccion");
    var texto = input.value.trim();

    if (texto === "") {
        mostrarError("Direccion", "Este campo es obligatorio.");
        return false;
    }
    if (texto.length < 5 || texto.length > 80) {
        mostrarError("Direccion", "Debe tener entre 5 y 80 caracteres.");
        return false;
    }
    if (!/[a-zA-ZáéíóúÁÉÍÓÚñÑ]/.test(texto)) {
        mostrarError("Direccion", "Debe contener al menos una letra.");
        return false;
    }
    if (!/\d/.test(texto)) {
        mostrarError("Direccion", "Debe contener al menos un número.");
        return false;
    }
    if (!/^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s.,°º#/-]+$/.test(texto)) {
        mostrarError("Direccion", "Solo se permiten letras, números y símbolos básicos (, . ° º # / -).");
        return false;
    }
    limpiarError("Direccion");
    return true;
}

function validarEmail() {
    var email = document.getElementById("Email").value.trim();
    var expresion = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (email === "") {
        mostrarError("Email", "Debe ingresar un correo.");
        return false;
    } else if (!expresion.test(email)) {
        mostrarError("Email", "Correo inválido.");
        return false;
    }

    limpiarError("Email");
    return true;
}

function validarPassword() {
    var pass1 = document.getElementById("Clave1").value;
    var pass2 = document.getElementById("Clave2").value;

    if (pass1 === "" || pass2 === "") {
        mostrarError("Clave2", "Debe completar ambos campos.");
        return false;
    } else if (pass1 !== pass2) {
        mostrarError("Clave2", "Las contraseñas no coinciden.");
        return false;
    } else if (pass1.length < 6) {
        mostrarError("Clave2", "Debe tener al menos 6 caracteres.");
        return false;
    } else if (!/[A-Z]/.test(pass1)) {
        mostrarError("Clave2", "Debe contener al menos una mayúscula.");
        return false;
    } else if (!/[0-9]/.test(pass1)) {
        mostrarError("Clave2", "Debe contener al menos un número.");
        return false;
    }

    limpiarError("Clave2");
    return true;
}

function validarFormularioRegistro(evento) {
    evento.preventDefault();

    var okNombre = validarNombre();
    var okApellido = validarApellido();
    var okDireccion = validarDireccion();
    var okEmail = validarEmail();
    var okPassword = validarPassword();

    if (okNombre && okApellido && okDireccion && okEmail && okPassword) {
        usuarioNombre = document.getElementById("Nombre").value + " " + document.getElementById("Apellido").value;
        if (typeof actualizarHeader === "function") {
            actualizarHeader();
        }
        document.querySelector("form").reset();
    }
}

function prepararMensajesDeError() {
    var ids = ["Nombre", "Apellido", "Direccion", "Email", "Clave2"];
    for (var i = 0; i < ids.length; i++) {
        var campo = document.getElementById(ids[i]);
        if (!document.getElementById("error-" + ids[i])) {
            var span = document.createElement("span");
            span.id = "error-" + ids[i];
            span.style.display = "block";
            span.style.marginTop = "4px";
            campo.after(span);
        }
    }
}

document.addEventListener("DOMContentLoaded", function () {
    prepararMensajesDeError();
    var formulario = document.querySelector("form");
    formulario.addEventListener("submit", validarFormularioRegistro);
});