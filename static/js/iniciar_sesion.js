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

    if (pass.trim() === "") {
        error = "Debe ingresar una contraseña.";
    }

    var span = document.getElementById(idError);
    span.innerHTML = error;
    span.style.color = "red";

    return error === "";
}

async function validarFormularioLogin(evento) {
    var valido = true;

    if (!validarEmail("Email", "errorEmail")) valido = false;
    if (!validarPassword("Clave", "errorClave")) valido = false;

    // Siempre frenamos el submit normal (porque usamos AJAX)
    evento.preventDefault();

    if (!valido) {
        return;
    }

    // Si pasa validación -> hacemos login real contra Flask
    const email = document.getElementById("Email").value.trim();
    const pass = document.getElementById("Clave").value;

    // Mensaje general (lo creamos si no existe)
    let msg = document.getElementById("login-msg");
    if (!msg) {
        msg = document.createElement("p");
        msg.id = "login-msg";
        msg.style.marginTop = "10px";
        msg.style.color = "red";
        const form = document.querySelector("form");
        form.appendChild(msg);
    }
    msg.textContent = "";

    try {
        const resp = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, pass })
        });

        const data = await resp.json().catch(() => ({}));

        if (resp.ok && data.ok) {
            // Si querés mantener esto:
            usuarioEmail = email;
            if (typeof actualizarHeader === "function") {
                actualizarHeader();
            }

            window.location.href = data.redirect || "/";
            return;
        }

        msg.textContent = data.msg || "Email o contraseña incorrectos.";
    } catch (e) {
        msg.textContent = "No se pudo conectar con el servidor.";
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