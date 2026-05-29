# What To Create / Install Next

The Django app files are already created. The UI theme is DM Inventory Premium Operations Theme.

## 1. Install Python

Install Python 3.12 or 3.13 from:

https://www.python.org/downloads/windows/

During install, check:

```text
Add python.exe to PATH
```

## 2. Open a new PowerShell in this folder

```powershell
cd "C:\Users\Rosebeth Mapa\OneDrive\Documents\smart inventory 2"
```

## 3. Install packages

```powershell
python -m pip install -r requirements.txt
```

## 4. Create the local database

```powershell
python manage.py migrate
```

## 5. Create the admin account

```powershell
python manage.py create_admin_account
```

Admin login:

```text
admin / admin12345
```

## 6. Create demo users and sample products

```powershell
python manage.py seed_demo
```

Login accounts:

```text
admin / admin12345
owner / owner12345
staff / staff12345
```

## 7. Run the app

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000
```

## Preview Without Django

Open this file in a browser to see the dashboard design immediately:

```text
preview_dashboard.html
```
