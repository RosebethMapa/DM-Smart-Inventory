# DM Smart Inventory & Ordering System

A web-based management system developed for a small retail store as part of a Software Design course project.

Premium Django inventory app for small business stock, sales, low-stock alerts, reports, and printable receipts.

Theme: DM Inventory Premium Operations Theme.

Main purpose: customers or staff can order store items, the system calculates total and change, and stock automatically decreases after payment or completion.

## Stack

- Django backend and templates
- Supabase PostgreSQL through `DATABASE_URL`
- Django auth
- WhiteNoise static files
- SQLite fallback for local development

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and update values. For Supabase, use the pooled PostgreSQL connection string:

```env
DATABASE_URL=postgresql://postgres.xxx:password@aws-xxx.pooler.supabase.com:6543/postgres
SECRET_KEY=change-this
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
TELEGRAM_ORDER_NOTIFICATIONS=True
```

4. Run migrations and seed demo data:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py create_admin_account
python manage.py seed_demo
python manage.py runserver
```

Demo logins:

- `admin` / `admin12345`
- `owner` / `owner12345`
- `staff` / `staff12345`

## Features

- Login-protected dashboard
- Product management with categories, suppliers, SKU/barcode search, archive support
- Stock-in workflow with stock movement records
- Stock adjustment audit records
- POS sales screen with cart, totals, amount received, change, and balance due
- Customer/staff ordering menu with photo item cards
- Pending, paid, completed, and cancelled order statuses
- Order history cards for mobile
- Transaction-safe stock reduction on sale
- Low-stock and suggested reorder report
- Sales, profit, best-seller, and movement reports
- Premium responsive UI for phone and desktop
- Premium printable receipt screen
- Telegram notification after each successful order when `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are configured

## Deployment Notes

Recommended first deployment:

- Supabase for PostgreSQL
- Render, Railway, or Fly.io for Django
- WhiteNoise for static files

Vercel note:

Django is best hosted as a long-running backend on Render/Railway/Fly.io. If using Vercel later, put a Next.js frontend on Vercel and keep Django as a separate API:

```text
Vercel frontend -> Django API -> Supabase PostgreSQL
```

Do not expose Supabase secret keys in frontend code. Keep business rules, stock updates, and audit logging on the Django side.
