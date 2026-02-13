async function postJSON(url, data) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data || {}),
  });

  const json = await res.json().catch(() => ({}));

  if (!res.ok) {
    if (json && json.redirect) window.location.href = json.redirect;
    throw new Error(json.msg || "Error");
  }
  return json;
}

async function refreshCartCount() {
  try {
    const res = await fetch("/api/cart/get");
    const json = await res.json().catch(() => null);
    if (res.ok && json && json.ok) {
      const countEl = document.getElementById("cartCount");
      if (countEl) countEl.textContent = json.count || 0;
    }
  } catch (e) {
    // silencioso
  }
}

document.addEventListener("DOMContentLoaded", () => {
  refreshCartCount();

  const btn = document.getElementById("btnAddCart");
  const sel = document.getElementById("Sabores");
  const err = document.getElementById("error-sabor");

  if (!btn) return;

  btn.addEventListener("click", async () => {
    const id_producto = parseInt(btn.getAttribute("data-id") || "0", 10);
    const sabor = (sel && sel.value) ? sel.value.trim() : "";

    if (!sabor) {
      if (err) err.textContent = "Elegí un sabor.";
      return;
    }
    if (err) err.textContent = "";

    try {
      const data = await postJSON("/api/cart/add", { id_producto, sabor });
      const countEl = document.getElementById("cartCount");
      if (countEl) countEl.textContent = data.count || 0;

      // opcional: te lo mando al carrito directo
      window.location.href = "/carrito";
    } catch (e) {
      alert(e.message);
    }
  });
});