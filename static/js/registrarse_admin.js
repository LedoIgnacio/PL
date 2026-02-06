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

// Valida NOMBRE
function validarNombre() {
    var texto = document.getElementById("Nombre").value.trim();
    var error = "";

    if (texto === "") {
        error = "Este campo es obligatorio.";
    } else if (texto.charAt(0) !== texto.charAt(0).toUpperCase()) {
        error = "Debe comenzar con mayúscula.";
    }

    if (error !== "") {
        mostrarError("Nombre", error);
        return false;
    }

    limpiarError("Nombre");
    return true;
}

// Valida APELLIDO
function validarApellido() {
    var texto = document.getElementById("Apellido").value.trim();
    var error = "";

    if (texto === "") {
        error = "Este campo es obligatorio.";
    } else if (texto.charAt(0) !== texto.charAt(0).toUpperCase()) {
        error = "Debe comenzar con mayúscula.";
    }

    if (error !== "") {
        mostrarError("Apellido", error);
        return false;
    }

    limpiarError("Apellido");
    return true;
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
    var pass1 = document.getElementById("Clave1").value;
    var pass2 = document.getElementById("Clave2").value;
    var error = "";

    if (pass1 !== pass2) {
        error = "Las contraseñas no coinciden.";
    } else if (pass1.length < 6) {
        error = "Debe tener al menos 6 caracteres.";
    } else if (!/[A-Z]/.test(pass1)) {
        error = "Debe contener al menos una mayúscula.";
    } else if (!/[0-9]/.test(pass1)) {
        error = "Debe contener al menos un número.";
    }

    if (error !== "") {
        mostrarError("Clave2", error);
        return false;
    }

    limpiarError("Clave2");
    return true;
}

function validarFormularioAdmin(evento) {
    evento.preventDefault();

    var okNombre = validarNombre();
    var okApellido = validarApellido();
    var okEmail = validarEmail();
    var okPassword = validarPassword();

    if (okNombre && okApellido && okEmail && okPassword) {
        usuarioNombre = document.getElementById("Nombre").value + " " + document.getElementById("Apellido").value;
        esAdmin = true;

        if (typeof actualizarHeader === "function") {
            actualizarHeader();
        }

        mostrarExito("Registro exitoso.");
        document.querySelector("form").reset();
    }
}

function prepararMensajesDeError() {
    var campos = ["Nombre", "Apellido", "Email", "Clave2"];
    for (var i = 0; i < campos.length; i++) {
        if (!document.getElementById("error-" + campos[i])) {
            var span = document.createElement("span");
            span.id = "error-" + campos[i];
            span.style.display = "block";
            span.style.marginTop = "5px";
            document.getElementById(campos[i]).after(span);
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
    formulario.addEventListener("submit", validarFormularioAdmin);
});