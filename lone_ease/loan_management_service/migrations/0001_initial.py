# Generated by Django 3.2.11 on 2023-07-18 06:32

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserInformation",
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
                ("name", models.CharField(max_length=128)),
                ("email", models.CharField(max_length=64)),
                ("annual_income", models.FloatField()),
                ("aadhar_id", models.CharField(max_length=64)),
            ],
        ),
    ]
