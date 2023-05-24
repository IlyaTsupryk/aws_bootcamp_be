# Generated by Django 4.2.1 on 2023-05-14 14:40

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Nft",
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
                ("name", models.CharField(max_length=512)),
                ("description", models.TextField()),
                ("owner", models.CharField(max_length=512)),
                ("size", models.IntegerField()),
                ("price", models.IntegerField()),
            ],
        ),
    ]
