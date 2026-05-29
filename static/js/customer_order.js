const cart = new Map();
const money = new Intl.NumberFormat("en-PH", { style: "currency", currency: "PHP" });

function renderCart() {
  const lines = document.querySelector("#cart-lines");
  const hidden = document.querySelector("#id_cart");
  const submit = document.querySelector("#submit-order");
  lines.innerHTML = "";
  let subtotal = 0;

  cart.forEach((item) => {
    const lineTotal = item.price * item.quantity;
    subtotal += lineTotal;
    const row = document.createElement("div");
    row.className = "customer-cart-line cart-line";
    row.innerHTML = `
      ${item.image ? `<img src="${item.image}" alt="">` : ""}
      <div><strong>${item.name}</strong><span>${money.format(item.price)}</span></div>
      <input type="number" min="1" max="${item.stock}" value="${item.quantity}" data-qty="${item.id}">
      <button type="button" data-remove="${item.id}">Remove</button>
    `;
    lines.appendChild(row);
  });

  hidden.value = JSON.stringify([...cart.values()].map((item) => ({ id: item.id, quantity: item.quantity })));
  document.querySelector("#customer-total").textContent = money.format(subtotal);
  submit.disabled = cart.size === 0;
}

document.querySelector("#customer-product-grid").addEventListener("click", (event) => {
  const tile = event.target.closest(".customer-product-card");
  if (!tile) return;

  const item = {
    id: Number(tile.dataset.id),
    name: tile.dataset.name,
    price: Number(tile.dataset.price),
    stock: Number(tile.dataset.stock),
    image: tile.dataset.image || "",
    quantity: 1,
  };

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

function filterProducts() {
  const query = document.querySelector("#customer-search").value.toLowerCase();
  const category = document.querySelector("#customer-category")?.value || "";
  document.querySelectorAll(".customer-product-card").forEach((tile) => {
    const text = `${tile.dataset.name} ${tile.dataset.sku} ${tile.dataset.category}`.toLowerCase();
    const categoryMatch = !category || tile.dataset.categoryId === category;
    tile.style.display = text.includes(query) && categoryMatch ? "" : "none";
  });
  document.querySelectorAll(".order-product-card").forEach((tile) => {
    const text = `${tile.dataset.name} ${tile.dataset.sku} ${tile.dataset.category}`.toLowerCase();
    tile.style.display = text.includes(query) ? "" : "none";
  });
}

document.querySelector("#customer-search").addEventListener("input", filterProducts);
document.querySelector("#customer-category")?.addEventListener("change", filterProducts);
document.querySelector("#customer-filter-button")?.addEventListener("click", filterProducts);

document.querySelectorAll("[data-filter]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll("[data-filter]").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    const filter = button.dataset.filter;
    document.querySelectorAll(".customer-product-card").forEach((tile) => {
      tile.style.display = !filter || tile.dataset.category === filter ? "" : "none";
    });
  });
});

renderCart();
