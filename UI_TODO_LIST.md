# DM Inventory Premium Operations Theme

The system must be mobile-first because Daisy Mapa will mostly use it on phone. Desktop should still look premium for admin and setup work.

## Brand

- Logo text: `DM`
- App name: `DM Inventory`
- Optional subtitle: `Daisy Mapa Smart Inventory`

## Premium Color Theme

```css
--bg: #f4f7fb;
--surface: #ffffff;
--border: #d8e0ec;
--text: #0f172a;
--muted: #64748b;
--primary: #2563eb;
--success: #16a34a;
--warning: #d97706;
--danger: #dc2626;
--sidebar: #0f172a;
--sidebar-active: #1e40af;
```

## Mobile-First Rules

- Design for phone first.
- No horizontal scrolling.
- Buttons and inputs minimum height: 44px.
- Important actions should be reachable with one thumb.
- Tables become cards on mobile.
- Desktop can expand into sidebar, grids, and tables.

## Navigation

- Desktop: dark navy sidebar with active blue state.
- Mobile: bottom navigation.
- Bottom nav items: Dashboard, Products, Sales, Stock, Reports.

## Dashboard

- Metric cards use 2 columns on phone.
- Important alerts appear near the top.
- Low-stock warning must be easy to see.
- Recent activity becomes stacked cards.

## Products

- Search bar stays at the top.
- Filter by category, supplier, and status.
- Add product button is blue on desktop and floating/sticky on mobile.
- Mobile product cards show product name, stock, price, status, and quick edit.

## Sales POS

- Most important mobile screen.
- Product search at the top.
- Product results as tappable cards.
- Cart below product list on mobile.
- Quantity inputs are large.
- Checkout button sticky at bottom.
- Cash received and change are big and clear.

## Stock In

- Large product selector/search.
- Big quantity input.
- Save button easy to tap.
- Show current stock before saving in a future enhancement.

## Reports

- Reports use cards on mobile.
- Show daily sales, profit, and low stock first.
- Avoid wide tables on phone.

## Empty States And Toasts

- No sales yet.
- No low stock.
- No products found.
- No reports available.
- Product saved.
- Stock added.
- Sale completed.
- Low stock warning.
- Error messages.
