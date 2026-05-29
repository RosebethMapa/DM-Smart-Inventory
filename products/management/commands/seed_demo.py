from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from dashboard.models import BusinessSettings
from products.models import Category, Product, Supplier
from stock.services import add_stock


class Command(BaseCommand):
    help = "Create demo users, products, suppliers, and opening stock."

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={"is_staff": True, "is_superuser": True, "email": "admin@example.com"},
        )
        admin.set_password("admin12345")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        owner, _ = User.objects.get_or_create(username="owner", defaults={"is_staff": True, "is_superuser": True})
        owner.set_password("owner12345")
        owner.is_staff = True
        owner.is_superuser = True
        owner.save()

        staff, _ = User.objects.get_or_create(username="staff")
        staff.set_password("staff12345")
        staff.save()

        owner_group, _ = Group.objects.get_or_create(name="Owner")
        manager_group, _ = Group.objects.get_or_create(name="Manager")
        staff_group, _ = Group.objects.get_or_create(name="Staff")
        admin.groups.add(owner_group)
        owner.groups.add(owner_group)
        staff.groups.add(staff_group)

        BusinessSettings.objects.get_or_create(business_name="DM Inventory")
        groceries, _ = Category.objects.get_or_create(name="Groceries")
        drinks, _ = Category.objects.get_or_create(name="Drinks")
        supplier, _ = Supplier.objects.get_or_create(name="Main Supplier", defaults={"phone": "0917 000 0000"})

        samples = [
            ("Rice 1kg", "RICE-1KG", groceries, Decimal("45.00"), Decimal("58.00"), 25, 10, 20, "https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=700&q=80"),
            ("Cooking Oil 1L", "OIL-1L", groceries, Decimal("72.00"), Decimal("89.00"), 8, 8, 16, "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&w=700&q=80"),
            ("Coffee Sachet", "COFFEE-S", groceries, Decimal("5.00"), Decimal("8.00"), 80, 30, 50, "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=700&q=80"),
            ("Bottled Water", "WATER-500", drinks, Decimal("9.00"), Decimal("15.00"), 4, 12, 24, "https://images.unsplash.com/photo-1523362628745-0c100150b504?auto=format&fit=crop&w=700&q=80"),
            ("Iced Tea", "TEA-250", drinks, Decimal("18.00"), Decimal("28.00"), 18, 10, 20, "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=700&q=80"),
        ]
        for name, sku, category, cost, price, stock, reorder, reorder_qty, image_url in samples:
            product, created = Product.objects.get_or_create(
                sku=sku,
                defaults={
                    "name": name,
                    "category": category,
                    "supplier": supplier,
                    "cost_price": cost,
                    "selling_price": price,
                    "reorder_level": reorder,
                    "reorder_quantity": reorder_qty,
                    "unit_type": "piece",
                    "image_url": image_url,
                },
            )
            if not product.image_url:
                product.image_url = image_url
                product.save(update_fields=["image_url", "updated_at"])
            if created:
                add_stock(product=product, quantity=stock, supplier=supplier, cost_per_unit=cost, reference="Opening stock", user=owner)

        self.stdout.write(self.style.SUCCESS("Demo data ready. Admin: admin / admin12345. Owner: owner / owner12345. Staff: staff / staff12345"))
