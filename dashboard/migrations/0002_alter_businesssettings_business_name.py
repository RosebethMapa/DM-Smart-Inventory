from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="businesssettings",
            name="business_name",
            field=models.CharField(default="DM Inventory", max_length=160),
        ),
    ]
