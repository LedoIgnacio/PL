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

function renderCart(items, total, count) {
  const lista = document.getElementById("listaProductos");
  const totalEl = document.getElementById("cartTotal");
  const countEl = document.getElementById("cartCount");

  totalEl.textContent = total || 0;
  countEl.textContent = count || 0;

  if (!items || items.length === 0) {
    lista.innerHTML = `<p style="color:white; padding: 20px;">Tu carrito está vacío.</p>`;
    return;
  }

  lista.innerHTML = items.map(it => `
    <div class="Item-carrito" data-key="${it.key}">
      <img src="${it.imagen}" alt="${it.nombre}">
      <div class="Info">
        <h3>${it.nombre}</h3>
        <p>Sabor: ${it.sabor}</p>
        <p>Precio: $${it.precio}</p>

        <div class="Cantidad-control">
          <button class="btn-cantidad" data-action="dec">-</button>
          <input type="number" value="${it.cantidad}" min="1" class="input-cantidad">
          <button class="btn-cantidad" data-action="inc">+</button>
        </div>
      </div>

      <button class="Eliminar" data-action="remove">
        <i class="fa-solid fa-trash-can"></i>
      </button>
    </div>
  `).join("");
}

document.addEventListener("click", async (e) => {
  const btn = e.target.closest("[data-action]");
  if (!btn) return;

  const item = btn.closest(".Item-carrito");
  if (!item) return;

  const key = item.getAttribute("data-key");
  const action = btn.getAttribute("data-action");

  try {
    if (action === "inc" || action === "dec") {
      const data = await postJSON("/api/cart/update", { key, action });
      renderCart(data.items, data.total, data.count);
    }

    if (action === "remove") {
      const data = await postJSON("/api/cart/remove", { key });
      renderCart(data.items, data.total, data.count);
    }
  } catch (err) {
    console.log(err);
    alert(err.message);
  }
});

document.addEventListener("change", async (e) => {
  const input = e.target.closest(".input-cantidad");
  if (!input) return;

  const item = input.closest(".Item-carrito");
  const key = item.getAttribute("data-key");

  let qty = parseInt(input.value || "1", 10);
  if (isNaN(qty) || qty < 1) qty = 1;

  try {
    const data = await postJSON("/api/cart/update", { key, action: "set", qty });
    renderCart(data.items, data.total, data.count);
  } catch (err) {
    console.log(err);
    alert(err.message);
  }
});