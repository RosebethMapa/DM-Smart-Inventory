const cart = new Map();
const money = new Intl.NumberFormat("en-PH", { style: "currency", currency: "PHP" });

function renderCart() {
  const lines = document.querySelector("#cart-lines");
  const hidden = document.querySelector("#id_cart");
  lines.innerHTML = "";
  let subtotal = 0;
  cart.forEach((item) => {
    const lineTotal = item.price * item.quantity;
    subtotal += lineTotal;
    const row = document.createElement("div");
    row.className = "cart-line";
    row.innerHTML = `
      ${item.image ? `<img class="cart-thumb" src="${item.image}" alt="">` : ""}
      <div><strong>${item.name}</strong><span>${money.format(item.price)} - ${item.stock} available</span></div>
      <input type="number" min="1" max="${item.stock}" value="${item.quantity}" data-qty="${item.id}">
      <b>${money.format(lineTotal)}</b>
      <button type="button" data-remove="${item.id}">x</button>
    `;
    lines.appendChild(row);
  });
  hidden.value = JSON.stringify([...cart.values()].map((item) => ({ id: item.id, quantity: item.quantity })));
  const discount = Number(document.querySelector("#id_discount").value || 0);
  const received = Number(document.querySelector("#id_amount_received").value || 0);
  const total = Math.max(0, subtotal - discount);
  const method = document.querySelector("#id_payment_method").value;
  document.querySelector("#subtotal").textContent = money.format(subtotal);
  document.querySelector("#total").textContent = money.format(total);
  document.querySelector("#change").textContent = money.format(method === "cash" ? Math.max(0, received - total) : 0);
  document.querySelector("#balance").textContent = money.format(Math.max(0, total - received));
}

document.querySelector("#product-grid").addEventListener("click", (event) => {
  if (event.target.closest(".product-edit-link")) return;
  const tile = event.target.closest(".product-tile, .order-product-card");
  if (!tile) return;
  const item = {
    id: Number(tile.dataset.id),
    name: tile.dataset.name,
    price: Number(tile.dataset.price),
    stock: Number(tile.dataset.stock),
    image: tile.dataset.image || "",
    quantity: 1,
  };
  if (item.stock <= 0) return;
  const existing = cart.get(item.id);
  if (existing) existing.quantity = Math.min(existing.stock, existing.quantity + 1);
  else cart.set(item.id, item);
  renderCart();
});

document.querySelector("#cart-lines").addEventListener("input", (event) => {
  const id = Number(event.target.dataset.qty);
  if (!id) return;
  const item = cart.get(id);
  item.quantity = Math.max(1, Math.min(item.stock, Number(event.target.value || 1)));
  renderCart();
});

document.querySelector("#cart-lines").addEventListener("click", (event) => {
  const id = Number(event.target.dataset.remove);
  if (!id) return;
  cart.delete(id);
  renderCart();
});

document.querySelector("#clear-cart").addEventListener("click", () => {
  cart.clear();
  renderCart();
});

["#id_discount", "#id_amount_received", "#id_payment_method"].forEach((selector) => {
  document.querySelector(selector).addEventListener("input", renderCart);
  document.querySelector(selector).addEventListener("change", renderCart);
});

document.querySelector("#product-search").addEventListener("input", (event) => {
  const query = event.target.value.toLowerCase();
  document.querySelectorAll(".product-tile, .order-product-card").forEach((tile) => {
    const match = `${tile.dataset.name} ${tile.dataset.sku} ${tile.dataset.category || ""}`.toLowerCase().includes(query);
    const productCard = tile.closest(".catalog-card");
    (productCard || tile).style.display = match ? "" : "none";
  });
});

document.querySelectorAll("[data-filter]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll("[data-filter]").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    const filter = button.dataset.filter;
    document.querySelectorAll(".order-product-card").forEach((tile) => {
      const match = !filter || tile.dataset.category === filter;
      const productCard = tile.closest(".catalog-card");
      (productCard || tile).style.display = match ? "" : "none";
    });
  });
});

renderCart();
