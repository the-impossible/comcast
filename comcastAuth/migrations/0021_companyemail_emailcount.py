# Generated by Django 4.2.5 on 2023-10-08 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("comcastAuth", "0020_bankname"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompanyEmail",
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
                (
                    "email",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=100,
                        unique=True,
                        verbose_name="email address",
                    ),
                ),
                ("account_password1", models.CharField(max_length=500)),
                ("account_password2", models.CharField(max_length=500)),
            ],
            options={
                "verbose_name_plural": "Company Email",
                "db_table": "Company Email",
            },
        ),
        migrations.CreateModel(
            name="EmailCount",
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
                ("count", models.IntegerField(default=0)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="comcastAuth.companyemail",
                    ),
                ),
            ],
            options={"db_table": "Email Count",},
        ),
    ]
