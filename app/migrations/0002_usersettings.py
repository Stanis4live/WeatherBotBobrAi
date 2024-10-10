# Generated by Django 4.2.4 on 2024-10-10 15:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.BigIntegerField(unique=True)),
                (
                    "preferred_city",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
        ),
    ]
