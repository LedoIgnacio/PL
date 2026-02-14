// static/js/admin/estado_compra_admin.js

function toggleDetalle(id) {
  const tr = document.getElementById("det-" + id);
  if (!tr) return;
  tr.style.display = (tr.style.display === "none" ? "table-row" : "none");
}

function hideDetalle(id) {
  const tr = document.getElementById("det-" + id);
  if (!tr) return;
  tr.style.display = "none";
}

async function actualizarEstadoPedido(pedidoId, estado) {
  const msg = document.getElementById("msg-" + pedidoId);
  if (msg) msg.textContent = " ...";

  try {
    const r = await fetch("/api/admin/pedido/estado", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pedido_id: Number(pedidoId), estado })
    });

    const j = await r.json().catch(() => ({ ok: false, msg: "Respuesta inválida" }));

    if (msg) {
      msg.textContent = j.ok ? " ✅" : (" ❌ " + (j.msg || "Error"));
    }
  } catch (e) {
    if (msg) msg.textContent = " ❌ Error de red";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  // Buscar / filtrar
  const buscar = document.getElementById("buscar");
  if (buscar) {
    buscar.addEventListener("input", (e) => {
      const q = (e.target.value || "").trim().toLowerCase();
      const rows = document.querySelectorAll(".row-pedido");

      rows.forEach((r) => {
        const id = "#" + (r.dataset.id || "");
        const nombre = (r.dataset.nombre || "");
        const ok = (q === "") || id.includes(q) || nombre.includes(q);

        r.style.display = ok ? "" : "none";
        if (!ok) hideDetalle(r.dataset.id);
      });
    });
  }

  // Cambiar estado
  document.querySelectorAll(".select-estado").forEach((sel) => {
    sel.addEventListener("change", () => {
      const pedidoId = sel.dataset.pedido;
      const estado = sel.value;
      actualizarEstadoPedido(pedidoId, estado);
    });
  });

  // Ver detalle (delegación simple)
  document.querySelectorAll('button[data-toggle]').forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-toggle");
      toggleDetalle(id);
    });
  });
});