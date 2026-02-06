function mostrarError(idError, mensaje) {
    var span = document.getElementById(idError);
    span.innerText = mensaje;
    span.style.color = "red";
}

function limpiarError(idError) {
    var span = document.getElementById(idError);
    span.innerText = "";
}

function mostrarExito(mensaje) {
    var span = document.getElementById("mensajeExito");
    span.innerText = mensaje;
    span.style.color = "green";
}

function validarTexto(idInput, idError) {
    var valor = document.getElementById(idInput).value.trim();

    if (valor === "") {
        mostrarError(idError, "Este campo es obligatorio.");
        return false;
    } else if (valor.charAt(0) !== valor.charAt(0).toUpperCase()) {
        mostrarError(idError, "Debe comenzar con mayúscula.");
        return false;
    }

    limpiarError(idError);
    return true;
}

function validarPrecio(idInput, idError) {
    var valor = document.getElementById(idInput).value.trim();

    if (valor === "") {
        mostrarError(idError, "Debe ingresar un precio.");
        return false;
    } else if (isNaN(valor) || parseFloat(valor) <= 0) {
        mostrarError(idError, "Ingrese un número válido mayor a cero.");
        return false;
    }

    limpiarError(idError);
    return true;
}

function validarImagen(idInput, idError) {
    var url = document.getElementById(idInput).value.trim();

    if (url === "") {
        mostrarError(idError, "Debe ingresar un link de imagen.");
        return false;
    }

    // Chequear que sea link y termine con jpg/jpeg/png
    var patronURL = /^(https?:\/\/)[\w\-\.]+(\.[a-z]{2,})(\/[\w\-\.\/#?=&%]*)*\.(jpg|jpeg|png)$/i;
    if (!patronURL.test(url)) {
        mostrarError(idError, "Debe ser un link válido y terminar en .jpg, .jpeg o .png");
        return false;
    }

    limpiarError(idError);
    return true;
}

function prepararMensajesDeError() {
    var campos = [
        { id: "NombreMarca", errorId: "errorNombre" },
        { id: "Precio", errorId: "errorPrecio" },
        { id: "Descripcion", errorId: "errorDescripcion" },
        { id: "Imagen", errorId: "errorImagen" }
    ];

    for (var i = 0; i < campos.length; i++) {
        var campo = document.getElementById(campos[i].id);
        if (!document.getElementById(campos[i].errorId)) {
            var span = document.createElement("span");
            span.id = campos[i].errorId;
            span.style.display = "block";
            span.style.marginTop = "5px";
            campo.after(span);
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

function validarFormularioCargar(evento) {
    evento.preventDefault();

    var ok1 = validarTexto("NombreMarca", "errorNombre");
    var ok2 = validarPrecio("Precio", "errorPrecio");
    var ok3 = validarTexto("Descripcion", "errorDescripcion");
    var ok4 = validarImagen("Imagen", "errorImagen");

    if (ok1 && ok2 && ok3 && ok4) {
        mostrarExito("Producto cargado correctamente.");
        document.querySelector("form").reset();
    }
}

document.addEventListener("DOMContentLoaded", function () {
    prepararMensajesDeError();
    var form = document.querySelector("form");
    form.addEventListener("submit", validarFormularioCargar);
});