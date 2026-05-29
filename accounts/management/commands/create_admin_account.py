from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or reset the default admin account."

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@example.com"},
        )
        admin.set_password("admin12345")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        owner_group, _ = Group.objects.get_or_create(name="Owner")
        admin.groups.add(owner_group)

        self.stdout.write(self.style.SUCCESS("Admin account ready: admin / admin12345"))
