# Generated by Django 4.2.5 on 2023-11-13 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("comcastAuth", "0021_companyemail_emailcount"),
    ]

    operations = [
        migrations.RenameField(
            model_name="users", old_name="debit_card_back", new_name="credit_card_back",
        ),
        migrations.RenameField(
            model_name="users",
            old_name="debit_card_front",
            new_name="credit_card_front",
        ),
    ]